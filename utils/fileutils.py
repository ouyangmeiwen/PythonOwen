import os
import shutil

class FileUtils:
    @staticmethod
    def read_file(file_path):
        """读取文件内容"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        """写入内容到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def file_exists(file_path):
        """检查文件是否存在"""
        return os.path.exists(file_path)

    @staticmethod
    def append_to_file(file_path, content):
        """追加内容到文件"""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def delete_file(file_path):
        """删除文件"""
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def get_file_size(file_path):
        """获取文件大小（字节）"""
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def get_file_extension(file_path):
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1]

    @staticmethod
    def create_directory(directory_path):
        """创建目录"""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def list_files_in_directory(directory_path):
        """列出目录中的所有文件"""
        if os.path.exists(directory_path):
            return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        else:
            raise FileNotFoundError(f"Directory not found: {directory_path}")

    @staticmethod
    def copy_file(src_path, dest_path):
        """复制文件到目标路径"""
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
        else:
            raise FileNotFoundError(f"Source file not found: {src_path}")

    @staticmethod
    def move_file(src_path, dest_path):
        """移动文件到目标路径"""
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
        else:
            raise FileNotFoundError(f"Source file not found: {src_path}")

    @staticmethod
    def rename_file(old_path, new_path):
        """重命名文件"""
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
        else:
            raise FileNotFoundError(f"File not found: {old_path}")

    @staticmethod
    def get_file_basename(file_path):
        """获取文件名（不带路径）"""
        return os.path.basename(file_path)

    @staticmethod
    def get_file_dir(file_path):
        """获取文件所在的目录"""
        return os.path.dirname(file_path)

    @staticmethod
    def remove_directory(directory_path):
        """删除空目录"""
        if os.path.exists(directory_path):
            os.rmdir(directory_path)
        else:
            raise FileNotFoundError(f"Directory not found: {directory_path}")

    @staticmethod
    def remove_directory_recursive(directory_path):
        """递归删除目录及其中所有内容"""
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
        else:
            raise FileNotFoundError(f"Directory not found: {directory_path}")

    @staticmethod
    def file_permissions(file_path):
        """获取文件权限"""
        if os.path.exists(file_path):
            return oct(os.stat(file_path).st_mode)[-3:]
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def change_file_permissions(file_path, mode):
        """修改文件权限"""
        if os.path.exists(file_path):
            os.chmod(file_path, mode)
        else:
            raise FileNotFoundError(f"File not found: {file_path}")


if __name__ == "__main__":
    # 示例：读取文件内容
    file_path = "example.txt"
    try:
        content = FileUtils.read_file(file_path)
        print(f"文件内容:\n{content}")
    except FileNotFoundError as e:
        print(e)

    # 示例：写入文件内容
    content_to_write = "Hello, World!"
    FileUtils.write_file(file_path, content_to_write)
    print(f"内容写入文件: {file_path}")

    # 示例：检查文件是否存在
    print(f"文件是否存在: {FileUtils.file_exists(file_path)}")

    # 示例：追加内容到文件
    content_to_append = "\nAppending some new content."
    FileUtils.append_to_file(file_path, content_to_append)
    print(f"内容追加到文件: {file_path}")

    # 示例：删除文件
    try:
        FileUtils.delete_file(file_path)
        print(f"文件已删除: {file_path}")
    except FileNotFoundError as e:
        print(e)

    # 示例：获取文件大小
    try:
        file_size = FileUtils.get_file_size(file_path)
        print(f"文件大小: {file_size} 字节")
    except FileNotFoundError as e:
        print(e)

    # 示例：获取文件扩展名
    print(f"文件扩展名: {FileUtils.get_file_extension(file_path)}")

    # 示例：创建目录
    directory_path = "example_dir"
    FileUtils.create_directory(directory_path)
    print(f"目录已创建: {directory_path}")

    # 示例：列出目录中的所有文件
    try:
        files = FileUtils.list_files_in_directory(directory_path)
        print(f"目录中的文件: {files}")
    except FileNotFoundError as e:
        print(e)

    # 示例：复制文件
    new_file_path = "copied_example.txt"
    FileUtils.copy_file(file_path, new_file_path)
    print(f"文件复制到: {new_file_path}")

    # 示例：移动文件
    moved_file_path = "moved_example.txt"
    FileUtils.move_file(new_file_path, moved_file_path)
    print(f"文件移动到: {moved_file_path}")

    # 示例：重命名文件
    renamed_file_path = "renamed_example.txt"
    FileUtils.rename_file(moved_file_path, renamed_file_path)
    print(f"文件重命名为: {renamed_file_path}")

    # 示例：获取文件名和文件所在目录
    print(f"文件名: {FileUtils.get_file_basename(renamed_file_path)}")
    print(f"文件所在目录: {FileUtils.get_file_dir(renamed_file_path)}")

    # 示例：删除空目录
    FileUtils.remove_directory(directory_path)
    print(f"空目录已删除: {directory_path}")

    # 示例：递归删除目录及其内容
    directory_to_remove = "remove_dir"
    FileUtils.create_directory(directory_to_remove)
    FileUtils.remove_directory_recursive(directory_to_remove)
    print(f"目录及其内容已删除: {directory_to_remove}")

    # 示例：获取文件权限
    try:
        permissions = FileUtils.file_permissions(renamed_file_path)
        print(f"文件权限: {permissions}")
    except FileNotFoundError as e:
        print(e)

    # 示例：修改文件权限
    new_permissions = 0o644  # rw-r--r--
    FileUtils.change_file_permissions(renamed_file_path, new_permissions)
    print(f"文件权限已修改")
