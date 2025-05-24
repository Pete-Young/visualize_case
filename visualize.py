# import pandas as pd
# import open3d as o3d
# import pyvista as pv
# # 读取数据
# data = pd.read_excel("wuhan_fit.xls")  # 如果是 Excel，用 pd.read_excel()
# points = data[["x", "y", "z"]].values
#
# # 创建点云
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
#
# # 预处理（可选）
# pcd = pcd.voxel_down_sample(voxel_size=0.05)
# pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
#
# # 计算法线
# pcd.estimate_normals()
#
# # 泊松重建
# mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
#
# # 保存并可视化
# o3d.io.write_triangle_mesh("reconstructed_mesh.ply", mesh)
# o3d.visualization.draw_geometries([mesh])

import pandas as pd
import pyvista as pv
import numpy as np

# 读取数据
data = pd.read_excel("wuhan_fit.xls")
# 生成示例数据
points = data[["x", "y", "z"]].values  # 转换为NumPy数组
mesh = pv.PolyData(points).delaunay_2d()
mesh["Height"] = points[:, 2]

scale_factor = 10
points[:, 2] *= scale_factor  # Z 列放大

# 创建点云并生成网格
cloud = pv.PolyData(points)
mesh = cloud.delaunay_2d()

# 添加渐变色（基于 Z 值）
mesh["Height"] = points[:, 2]
mesh["Enhanced_Height"] = np.exp(points[:, 2])  # 指数放大差异
# 可视化设置
plotter = pv.Plotter()

# 设置渐变背景（从深蓝色到浅蓝色）
# plotter.set_background("navy", top="lightblue")

# 添加网格模型（颜色基于 Z 值）
mesh["Height"] = mesh.points[:, 2]
# plotter.add_mesh(
#     mesh,
#     scalars="Height",
#     cmap="viridis",
#     show_edges=False,
#     scalar_bar_args={"title": "高度 (m)"}
# )
#
# plotter.add_mesh(
#     mesh,
#     scalars="Height",
#     cmap="rainbow",          # 颜色映射方案（viridis、plasma、inferno 等）
#     show_edges=False,
#     scalar_bar_args={
#         "title": "Z Value",  # 颜色条标题
#         "position_x": 0.85,  # 颜色条位置
#         "height": 0.5,
#         "width": 0.1,
#     },
# )

mesh["Enhanced_Height"] = np.exp(points[:, 2] - points[:, 2].min())

# 方法2：手动扩展颜色范围（比实际数据范围更大）
clim_min = points[:, 2].min() - 1  # 向下扩展1个单位
clim_max = points[:, 2].max() + 2  # 向上扩展2个单位

plotter.add_mesh(
    mesh,
    scalars="Enhanced_Height",  # 使用变换后的高度
    cmap="turbo",               # 高对比度颜色映射
    clim=[clim_min, clim_max],  # 强制颜色范围
    smooth_shading=True,        # 平滑着色
    specular=0.8,               # 高光强度（0-1）
    show_edges=False,           # 不显示网格线
    scalar_bar_args={
        "title": "增强高度",
        "shadow": True
    }
)

plotter.show_axes()          # 显示坐标轴
plotter.show()               # 显示窗口

# 保存结果
plotter.screenshot("vi_enhanced_z_visualization.png")
mesh.save("vi_enhanced_mesh.stl")