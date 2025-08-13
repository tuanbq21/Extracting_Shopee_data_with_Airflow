import unittest
from unittest.mock import patch, MagicMock
from airflow.models import DagBag
import os

class TestShopeeRatingsPipeline(unittest.TestCase):

    def setUp(self):
        # Load DAG từ file .py của bạn, đổi tên file nếu cần
        self.dagbag = DagBag(dag_folder=os.path.dirname(__file__), include_examples=False)
        self.dag = self.dagbag.get_dag('shopee_ratings_pipeline')

    def test_dag_loaded(self):
        self.assertIsNotNone(self.dag)
        self.assertEqual(len(self.dag.tasks), 3)

    @patch('your_dag_module.crawl_data')  # Thay your_dag_module bằng tên file .py chứa DAG (ko có .py)
    @patch('your_dag_module.transform_data')
    @patch('your_dag_module.load_data')
    def test_tasks_execute(self, mock_load, mock_transform, mock_crawl):
        # Giả lập các hàm không làm thật các thao tác
        mock_crawl.return_value = None
        mock_transform.return_value = None
        mock_load.return_value = None

        # Lấy các task
        crawl_task = self.dag.get_task('crawl')
        transform_task = self.dag.get_task('transform')
        load_task = self.dag.get_task('load')

        # Thực thi từng task (trong context airflow, gọi execute)
        crawl_task.execute({})
        mock_crawl.assert_called_once()

        transform_task.execute({})
        mock_transform.assert_called_once()

        load_task.execute({})
        mock_load.assert_called_once()

    def test_task_dependencies(self):
        crawl_task = self.dag.get_task('crawl')
        transform_task = self.dag.get_task('transform')
        load_task = self.dag.get_task('load')

        self.assertListEqual(crawl_task.downstream_task_ids, {'transform'})
        self.assertListEqual(transform_task.downstream_task_ids, {'load'})
        self.assertListEqual(load_task.downstream_task_ids, [])

if __name__ == '__main__':
    unittest.main()
