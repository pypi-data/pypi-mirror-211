# JSON 轉 GitHub Actions YAML
這個 Python 套件能將 JSON 格式轉化為 GitHub Actions 的 YAML 格式。

## 安裝
將 `json_to_github_actions.py` 放到您的專案資料夾中

## CLI 用法
```
python json_to_github_actions.py --json_file [json_file] --yaml_file [yaml_file]
```

範例：
```bash
python json_to_github_actions.py --json_file input.json --yaml_file output.yaml
```

輸入 `json_file` 是您的 JSON 檔案路徑，並將產生的 GitHub Actions YAML 檔案保存到給定的 `yaml_file` 路徑。

## 套件 import 用法
首先，將 `json_to_github_actions.py` 腳本導入您的專案。

```python
from json_to_github_actions import json_to_github_actions
```

然後您可以調用 `json_to_github_actions()` 函數將 JSON 輸入轉換為 YAML 格式。

```python
json_data = '''
{
  "repo_url": "https://github.com/user/repo",
  "script_dir": "scripts",
  "script_name": "main.py",
  "execution_environment": [
    {
      "language": "python",
      "version": "3.8",
      "installation_command": "pip install -r requirements.txt"
    }
  ],
  "json_parameters": [
    {"param1": "value1", "param2": 42},
    {"param1": "value2", "param2": 24}
  ],
  "max_parallel": 2
}
'''

yaml_data = json_to_github_actions(json_data)
```

這將把 JSON 格式的數據轉換為適用於 GitHub Actions 的 YAML 格式。之後，您可以選擇將 `yaml_data` 保存到檔案中。
