import json
from pathlib import Path
import requests
from cvat_sdk import Client, Config, models

CVAT_URL = 'http://localhost:8080'
AUTH_TOKEN = '38c6f78b36902f8c4e0014dff380bafd477240f0'

def main():
    client = Client(url=CVAT_URL, config=Config(verify_ssl=False))
    client.api_client.default_headers['Authorization'] = f'Token {AUTH_TOKEN}'

    r = requests.get(f'{CVAT_URL}/api/tasks', headers={'Authorization': f'Token {AUTH_TOKEN}'})
    existing_tasks = {t['name']: t['id'] for t in r.json().get('results', [])}
    print('Existing tasks in CVAT:', existing_tasks)

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'data' / 'manifest.json').read_text(encoding='utf-8'))['tasks']

    task_order = [
        'easy_semantic',
        'medium_instance',
        'hard_panoptic',
        'cp1_holes',
        'cp2_slice',
        'cp3_thin',
        'cp4_curb',
        'cp5_occlusion',
        'cp6_coverage'
    ]

    for task_name in task_order:
        if task_name in existing_tasks:
            print(f"Task '{task_name}' already exists (ID: {existing_tasks[task_name]}), skipping.")
            continue

        info = manifest[task_name]
        task_dir = root / 'data' / info['path']
        labels_file = task_dir / 'cvat-labels.json'
        labels = json.loads(labels_file.read_text(encoding='utf-8'))
        images = sorted(list((task_dir / 'images').glob('*.jpg')))

        print(f"Creating task '{task_name}' with {len(images)} images and {len(labels)} labels...")
        task = client.tasks.create_from_data(
            spec=models.TaskWriteRequest(
                name=task_name,
                labels=[models.PatchedLabelRequest(**l) for l in labels]
            ),
            resources=images,
            data_params={'image_quality': 70}
        )
        print(f"-> Created task '{task_name}' successfully with ID: {task.id}")

    print("\nAll tasks processing finished!")

if __name__ == '__main__':
    main()
