"""No-network tests for explicit submission locks and duplicate-charge prevention."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RENDERER = Path(__file__).with_name('metaso_h3_video.py')

class RenderGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'frame.png').write_bytes(b'fixture')
        (self.root / 'prompt.md').write_text('```text\nA quiet room.\n```')
        self.manifest = {'total_duration_seconds': 4}
        self.job = {'id': 'clip-01', 'duration_seconds': 4, 'prompt_file': 'prompt.md',
                    'references': [{'type': 'image', 'path': 'frame.png', 'role': 'first_frame', 'slot': 1}]}
        self.jobs = {'jobs': [self.job]}
    def tearDown(self):
        self.tmp.cleanup()
    def run_renderer(self, *flags):
        (self.root / 'project-manifest.json').write_text(json.dumps(self.manifest))
        (self.root / 'api-jobs.json').write_text(json.dumps(self.jobs))
        return subprocess.run([sys.executable, str(RENDERER), str(self.root), *flags],
                              capture_output=True, text=True)
    def test_disabled_examples_still_allow_readonly_plan(self):
        self.jobs['submission_enabled'] = False
        result = self.run_renderer('--dry-run', '--no-assemble')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['jobs'][0]['id'], 'clip-01')
        self.assertFalse((self.root / 'render-state.json').exists())
    def test_locks_stop_before_network_or_state_mutation(self):
        for source in [self.manifest, self.jobs, self.job]:
            with self.subTest(source=source):
                source['submission_enabled'] = False
                result = self.run_renderer('--no-assemble')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('submission', result.stderr)
                self.assertFalse((self.root / 'render-state.json').exists())
                del source['submission_enabled']
    def test_existing_tasks_cannot_be_overwritten_or_resubmitted(self):
        state = {'jobs': [{'id': 'clip-01', 'task_id': 'fixture-task', 'status': 'running'}]}
        path = self.root / 'render-state.json'
        original = json.dumps(state)
        path.write_text(original)
        result = self.run_renderer('--no-assemble')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Existing provider tasks', result.stderr)
        self.assertEqual(path.read_text(), original)

if __name__ == '__main__':
    unittest.main()
