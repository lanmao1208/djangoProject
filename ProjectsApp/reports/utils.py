# 创建生成器,获取文件流,每次获取数据是文件的字节数据(为防止文件过大导致的下载速度低,创建生成器进行迭代)
def get_file_content(filename, chunk_size=1024):
    with open(filename, encoding='utf-8') as file:
        while True:
            content = file.read(chunk_size)
            # 文件结尾,content为空就跳出循环
            if not content:
                break
            yield content