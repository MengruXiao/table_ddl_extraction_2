import streamlit as st
import pandas as pd


st.title('table_ddl_提取字段及其类型')

# 目前只支持redshift的ddl, snowflake或者mssql或者其他的后续再说
# 选择功能
function = st.selectbox('选择sql类型', ['redshift', 'snowflake'])

# 添加一个输入框和一个粘贴按钮
text_input = st.text_area('输入您的 DDL 语句', '')

if st.button('处理并导出'):

    if text_input:
        # 读取文件内容
        lines = text_input.splitlines()

        if function == 'redshift':
            columns = []
            for line in lines[1:]:
                if line.strip().startswith(')'):
                    break
                if ", " in line:
                    line = line.replace(', ', ',')
                parts = line.strip().split(' ')
                if len(parts) >= 2:
                    column_name = parts[0]
                    if parts[1] == 'character':
                        type = parts[2].replace('varying', 'varchar')
                    elif parts[1] == 'timestamp':
                        type = 'datetime'
                    elif parts[1] == 'integer':
                        type = 'int'
                    else:
                        type = parts[1]
                    columns.append((column_name, type))

            if columns:
                st.write('提取的字段及其类型:')
                df = pd.DataFrame(columns, columns=['column_name','type'])
                st.dataframe(df)
            else:
                st.warning('没有找到有效的字段定义。')

        else:

            st.warning('前面的道路以后再来探索吧~')

else:
    st.warning('请先输入ddl')