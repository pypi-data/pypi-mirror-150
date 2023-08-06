# 验证算法公平性与完整性
# 开始

# 传入pandas dateframe作为数据集
dataset = Analyse(pandas_dataframe)

# 验证完整性
result = Analyse.completeness(col_name)
# col_name 数据列名，返回有多少空值

# 验证公平性
dataset.new_test
# 将pandas_dataframe中的敏感属性所在列随机打乱，重新赋值，然后再进行实验

# 查看数据分布
dataset.dis_analyse('x', 'y')
# 输出y相对于x的分布图像

# 比较两次实验结果差异
dataset.compare(x, y)
# 输入两次结果x, y(二者均为torch向量)，比较KL散度，越大说明相差越大