import unittest
import os
from ai_agent_sdk import AIAgentSDK

class TestAIAgentSDK(unittest.TestCase):
    def setUp(self):
        os.environ['OPENAI_API_KEY'] = 'test_key'
        os.environ['AGENT_NAME'] = 'TestAgent'
        os.environ['GITHUB_TOKEN'] = 'test_token'
        os.environ['GITHUB_REPOSITORY_VISIBILITY'] = 'public'
        
    def test_execute_task_public(self):
        agent = AIAgentSDK()
        task = {'input': 'Test input'}
        result = agent.execute_task(task)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['processed_data'], 'Processed: Test input')
        
    def test_execute_task_private_unlicensed(self):
        os.environ['GITHUB_REPOSITORY_VISIBILITY'] = 'private'
        agent = AIAgentSDK()
        task = {'input': 'Test input'}
        result = agent.execute_task(task)
        self.assertEqual(result['status'], 'error')
        self.assertIn('Paid license required', result['error_message'])

if __name__ == '__main__':
    unittest.main()
