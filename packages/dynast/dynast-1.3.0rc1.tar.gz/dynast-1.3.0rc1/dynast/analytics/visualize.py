# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import math
from typing import List

import numpy as np
import pandas as pd
from scipy.spatial import Delaunay
from shapely.geometry import MultiLineString, MultiPoint, mapping
from shapely.ops import cascaded_union, polygonize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
# from dynast.supernetwork.supernetwork_registry import SUPERNET_METRICS

from dynast.utils import log


def frontier_builder(df, optimization_metrics, alpha=0, verbose=False):
    """
    Modified alphashape algorithm to draw Pareto Front for OFA search.
    Takes a DataFrame of column form [x, y] = [latency, accuracy]

    Params:
    df     - dataframe containing `optimization_metrics` columns at minimum
    alpha  - Dictates amount of tolerable 'concave-ness' allowed.
             A fully convex front will be given if 0 (also better for runtime)
    """
    if verbose:
        log.info('Running front builder')
    df = df[optimization_metrics]
    points = list(df.to_records(index=False))
    for i in range(len(points)):
        points[i] = list(points[i])
    points = MultiPoint(points)

    # TODO(macsz) Fix the line below in comment:
    # if len(points) < 4 or alpha <= 0:
    if alpha <= 0:
        if verbose:
            log.info('Alpha=0 -> convex hull')
        result = points.convex_hull
    else:
        coords = np.array([point.coords[0] for point in points])
        tri = Delaunay(coords)
        edges = set()
        edge_points = []
        edge_out = []

        # Loop over triangles
        for ia, ib, ic in tri.vertices:
            pa = coords[ia]
            pb = coords[ib]
            pc = coords[ic]

            # Lengths of sides of triangle
            a = math.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
            b = math.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
            c = math.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)

            # Semiperimeter of triangle
            s = (a + b + c) * 0.5

            # Area of triangle by Heron's formula
            # Precompute value inside square root to avoid unbound math error in
            # case of 0 area triangles.
            area = s * (s - a) * (s - b) * (s - c)

            if area > 0:
                area = math.sqrt(area)

                # Radius Filter
                if a * b * c / (4.0 * area) < 1.0 / alpha:
                    for i, j in itertools.combinations([ia, ib, ic], r=2):
                        if (i, j) not in edges and (j, i) not in edges:
                            edges.add((i, j))
                            edge_points.append(coords[[i, j]])

                            if coords[i].tolist() not in edge_out:
                                edge_out.append(coords[i].tolist())
                            if coords[j].tolist() not in edge_out:
                                edge_out.append(coords[j].tolist())

        # Create the resulting polygon from the edge points
        m = MultiLineString(edge_points)
        triangles = list(polygonize(m))
        result = cascaded_union(triangles)

    # Find multi-polygon boundary
    bound = list(mapping(result.boundary)['coordinates'])

    # Cutoff non-Pareto front points
    # note that extreme concave geometries will create issues if bi-sected by line
    df = pd.DataFrame(bound, columns=['x', 'y'])

    # y=mx+b
    left_point = (df.iloc[df.idxmin()[0]][0], df.iloc[df.idxmin()[0]][1])
    right_point = (df.iloc[df.idxmax()[1]][0], df.iloc[df.idxmax()[1]][1])
    m = (left_point[1] - right_point[1]) / (left_point[0] - right_point[0])
    b = left_point[1] - (m * left_point[0])

    df = df[df['y'] >= (m * df['x'] + b)]
    df.sort_values(by='x', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Cleanup - insure accuracy is always increasing with latency up the Pareto front
    best_acc = 0
    drop_list = []
    for i in range(len(df)):
        if df.iloc[i]['y'] > best_acc:
            best_acc = df.iloc[i]['y']
        else:
            drop_list.append(i)
    df.drop(df.index[drop_list], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.columns = optimization_metrics

    return df


def plot_search_progression(
        csv_path: str,
        plot_columns: List[str] = ['macs', 'accuracy_top1'],
        supernet_metrics: List[str] = ['params', 'latency', 'macs', 'accuracy_top1'],
        save_path: str=None,
    ):
    assert len(plot_columns) == 2, 'Only 2D plots are supported'

    df_dynas = pd.read_csv(csv_path)
    df_dynas.columns = ['config', 'date'] + supernet_metrics

    fig, ax = plt.subplots(figsize=(7,5))

    cm = plt.cm.get_cmap('viridis_r')
    count = [x for x in range(len(df_dynas))]

    ax.scatter(df_dynas[plot_columns[0]].values, df_dynas[plot_columns[1]].values, marker='^', alpha=0.8, c=count,
            cmap=cm, label='Discovered DNN Model', s=10)

    df_front = frontier_builder(df_dynas, plot_columns)
    ax.plot(
        df_front[plot_columns[0]].values,
        df_front[plot_columns[1]].values,
        '--',
        color='red',
        label='Pareto Frontier',
        linewidth=2,
    )

    ax.set_title('DyNAS-T Search Results\n OFA ResNet50 - Bug')
    ax.set_xlabel(plot_columns[0], fontsize=13)
    ax.set_ylabel(plot_columns[1], fontsize=13)
    ax.legend(fancybox=True, fontsize=10, framealpha=1, borderpad=0.2, loc='lower right')
    ax.grid(True, alpha=0.3)
    #ax.set_ylim(72,77.5)

    # ax.plot(1.75e10, 77.9, marker='*', markersize=10, color='red', label='ViT Supernet')

    # Eval Count bar
    norm = plt.Normalize(0, len(df_dynas))
    sm = ScalarMappable(norm=norm, cmap=cm)
    cbar = fig.colorbar(sm, ax=ax, shrink=0.85)
    cbar.ax.set_title("         Evaluation\n  Count", fontsize=8)

    fig.tight_layout(pad=2)

    if save_path is None:
        save_path = csv_path.replace('.csv', '.png')
    log.info(f'Search progression visualization saved to {save_path}')
    plt.savefig(save_path, dpi=300)


def plot_search_progression_2(
        csv_path_1: str,
        csv_path_2: str,
        plot_columns: List[str] = ['macs', 'accuracy_top1'],
        supernet_metrics: List[str] = ['params', 'latency', 'macs', 'accuracy_top1'],
        save_path: str=None,
    ):
    assert len(plot_columns) == 2, 'Only 2D plots are supported'

    # 1
    df_dynas = pd.read_csv(csv_path_1)
    df_dynas.columns = ['config', 'date'] + supernet_metrics

    fig, ax = plt.subplots(figsize=(7,5))

    cm = plt.cm.get_cmap('Oranges')
    count = [x for x in range(len(df_dynas))]

    ax.scatter(df_dynas[plot_columns[0]].values, df_dynas[plot_columns[1]].values, marker='^', alpha=0.8, c=count,
            cmap=cm, label='Discovered DNN Model - Bug', s=10)

    df_front = frontier_builder(df_dynas, plot_columns)
    ax.plot(
        df_front[plot_columns[0]].values,
        df_front[plot_columns[1]].values,
        '--',
        color='tab:orange',
        label='Pareto Frontier - Bug',
        linewidth=2,
    )

    # 2
    df_dynas = pd.read_csv(csv_path_2)
    df_dynas.columns = ['config', 'date'] + supernet_metrics

    # fig, ax = plt.subplots(figsize=(7,5))

    cm = plt.cm.get_cmap('Greens')
    count = [x for x in range(len(df_dynas))]

    ax.scatter(df_dynas[plot_columns[0]].values, df_dynas[plot_columns[1]].values, marker='^', alpha=0.8, c=count,
            cmap=cm, label='Discovered DNN Model - Fixed', s=10)

    df_front = frontier_builder(df_dynas, plot_columns)
    ax.plot(
        df_front[plot_columns[0]].values,
        df_front[plot_columns[1]].values,
        '--',
        color='tab:green',
        label='Pareto Frontier - Fixed',
        linewidth=2,
    )

    ax.set_title('DyNAS-T Search Results\n OFA ResNet50 - Bug')
    ax.set_xlabel(plot_columns[0], fontsize=13)
    ax.set_ylabel(plot_columns[1], fontsize=13)
    ax.legend(fancybox=True, fontsize=10, framealpha=1, borderpad=0.2, loc='lower right')
    ax.grid(True, alpha=0.3)
    #ax.set_ylim(72,77.5)

    # ax.plot(1.75e10, 77.9, marker='*', markersize=10, color='red', label='ViT Supernet')

    # Eval Count bar
    norm = plt.Normalize(0, len(df_dynas))
    sm = ScalarMappable(norm=norm, cmap=plt.cm.get_cmap('Greys'))
    cbar = fig.colorbar(sm, ax=ax, shrink=0.85)
    cbar.ax.set_title("         Evaluation\n  Count", fontsize=8)

    fig.tight_layout(pad=2)

    if save_path is None:
        save_path = csv_path_1.replace('.csv', '_comp.png')
    log.info(f'Search progression visualization saved to {save_path}')
    plt.savefig(save_path, dpi=300)


if __name__ == '__main__':
    # df_dynas = pd.read_csv('/localdisk/maciej/code/DyNAS-T-validate/bert_random.csv')[:evals]
    # df_dynas = pd.read_csv('/localdisk/maciej/code/DyNAS-T-validate/ofa_mbv3_linas_fr0.2.csv')
    # df_dynas = pd.read_csv('/localdisk/maciej/code/DyNAS-T-validate/bert_linas_column_fix.csv')
    plot_search_progression(
        # 'bert_linas_column_fix_2.csv',
        # 'bert_linas_main.csv',
        'results_ofaresnet50_linas_long_main.csv',
        # 'results_ofaresnet50_linas_long_ksed_fix.csv',
        # 'ofa_mbv3_d234_e346_k357_w1.0',
        plot_columns=['macs', 'accuracy_top1']
    )

    plot_search_progression_2(
        # 'bert_linas_column_fix_2.csv',
        # 'bert_linas_main.csv',
        'results_ofaresnet50_linas_long_main.csv',
        'results_ofaresnet50_linas_long_ksed_fix.csv',
        # 'ofa_mbv3_d234_e346_k357_w1.0',
        plot_columns=['macs', 'accuracy_top1']
    )