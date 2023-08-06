"""
Integration tests.

Table of Contents:
- Imports
- Test case directory and paths
- Expected events
- Test case class definition
"""

###########
# Imports #
###########

# Standard library imports
import json
import pandas as pd
import os
from pathlib import Path
import shutil
from typing import Dict, List

# Prism imports
import prism.tests.integration.integration_test_class as integration_test_class


#################################
# Test case directory and paths #
#################################

# Directory containing all prism_project.py test cases
TEST_CASE_WKDIR = os.path.dirname(__file__)
TEST_PROJECTS = Path(TEST_CASE_WKDIR) / 'test_projects'


###################
# Expected events #
###################

def _execution_events_modules(module_names_statuses: dict) -> list:
    """
    Create list for execution events

    args:
        module_names_statuses: dict mapping event_name --> event_status
    returns:
        list of execution events
    """
    results = []
    for k, v in module_names_statuses.items():
        results.append(f'ExecutionEvent - {k} - RUN')
        results.append(f'ExecutionEvent - {k} - {v}')
    return results


def _run_task_end_events(end_event_name: str) -> list:
    """
    Create list for events marking the end of the run task

    args:
        end_event_name: name of end event
    returns:
        list of events marking end of run task
    """
    return [
        'EmptyLineEvent',
        end_event_name,
        'SeparatorEvent'
    ]


# Starting events for a successful run task. We will only run tasks that successfully
# compile, since we have dealt with compile edge cases in the `test_compile` integration
# tests.
run_success_starting_events = [
    'SeparatorEvent',
    'TaskRunEvent',
    'CurrentProjectDirEvent',
    'EmptyLineEvent',
    'ExecutionEvent - parsing prism_project.py - RUN',
    'ExecutionEvent - parsing prism_project.py - DONE',
    'ExecutionEvent - module DAG - RUN',
    'ExecutionEvent - module DAG - DONE',
    'ExecutionEvent - creating pipeline, DAG executor - RUN',
    'ExecutionEvent - creating pipeline, DAG executor - DONE',
    'EmptyLineEvent'
]


simple_project_all_modules_expected_events = run_success_starting_events + \
    ['TasksHeaderEvent'] + \
    _execution_events_modules({'module03.py': 'ERROR'}) + \
    _run_task_end_events('PrismExceptionErrorEvent')

simple_project_no_null_all_modules_expected_events = run_success_starting_events + \
    ['TasksHeaderEvent'] + \
    _execution_events_modules({
        'module01.py': 'DONE',
        'module02.py': 'DONE',
        'module03.py': 'DONE',
        'module04.py': 'DONE',
    }) + _run_task_end_events('TaskSuccessfulEndEvent')


##############################
# Test case class definition #
##############################

class TestRunIntegration(integration_test_class.IntegrationTestCase):

    def test_simple_project_all_modules(self):
        """
        `prism run` on simple project with a null task output
        """
        self.maxDiff = None

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '004_simple_project'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Execute command
        args = ['run']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        self.assertTrue(Path(wkdir / '.compiled').is_dir())
        self.assertTrue(Path(wkdir / '.compiled' / 'manifest.json').is_file())

        # Check events
        self.assertEqual(
            ' | '.join(simple_project_all_modules_expected_events),
            runtask_run_results
        )

        # Check manifest.json
        manifest = self._load_manifest(Path(wkdir / '.compiled' / 'manifest.json'))
        module01_refs = self._load_module_refs("module01.py", manifest)
        module02_refs = self._load_module_refs("module02.py", manifest)
        module03_refs = self._load_module_refs("module03.py", manifest)
        self.assertEqual([], module01_refs)
        self.assertEqual('module01.py', module02_refs)
        self.assertEqual([], module03_refs)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_simple_project_no_null_all_modules(self):
        """
        `prism run` on simple project with no null task outputs
        """
        self.maxDiff = None

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '005_simple_project_no_null'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Execute command
        args = ['run']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        self.assertEqual(
            ' | '.join(simple_project_no_null_all_modules_expected_events),
            runtask_run_results
        )
        self.assertTrue(Path(wkdir / 'output' / 'module01.txt').is_file())
        self.assertTrue(Path(wkdir / 'output' / 'module02.txt').is_file())

        # Check contents
        module01_txt = self._file_as_str(Path(wkdir / 'output' / 'module01.txt'))
        module02_txt = self._file_as_str(Path(wkdir / 'output' / 'module02.txt'))
        self.assertEqual('Hello from module 1!', module01_txt)
        self.assertEqual(
            'Hello from module 1!' + '\n' + 'Hello from module 2!',
            module02_txt
        )

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_simple_project_no_null_subset(self):
        """
        `prism run` on simple project with no null task outputs
        """
        self.maxDiff = None

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '005_simple_project_no_null'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # ***************** #
        # Run only module 1 #
        # ***************** #

        # Expecatation: module 1 is the first module in the DAG. Therefore, we should
        # not encounter any errors with this command.
        args = ['run', '--modules', 'module01.py']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules({'module01.py': 'DONE'}) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), runtask_run_results)

        # Check the results of the output directory
        self.assertTrue(Path(wkdir / 'output' / 'module01.txt').is_file())
        self.assertFalse(Path(wkdir / 'output' / 'module02.txt').is_file())
        module01_txt = self._file_as_str(Path(wkdir / 'output' / 'module01.txt'))
        self.assertEqual('Hello from module 1!', module01_txt)

        # Check manifest
        self.assertTrue(Path(wkdir / '.compiled').is_dir())
        self.assertTrue(Path(wkdir / '.compiled' / 'manifest.json').is_file())
        manifest = self._load_manifest(Path(wkdir / '.compiled' / 'manifest.json'))
        module01_refs = self._load_module_refs("module01.py", manifest)
        module02_refs = self._load_module_refs("module02.py", manifest)
        module03_refs = self._load_module_refs("module03.py", manifest)
        module04_refs = self._load_module_refs("module04.py", manifest)
        self.assertEqual([], module01_refs)
        self.assertEqual('module01.py', module02_refs)
        self.assertEqual('module02.py', module03_refs)
        self.assertEqual('module03.py', module04_refs)

        # **************** #
        # Execute module 2 #
        # **************** #

        # Expecatation: module 2 depends on module 1. However, since we just ran module
        # 1, and the output of module 1 is stored in a target, we do not need to re-run
        # module 1 in order to run module 2. Therefore, we should not encounter any
        # errors with this command.

        # Execute command
        args = ['run', '--modules', 'module02.py', '--full-tb']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules({'module02.py': 'DONE'}) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), runtask_run_results)

        # Check the results of the output directory
        self.assertTrue(Path(wkdir / 'output' / 'module02.txt').is_file())
        with open(Path(wkdir / 'output' / 'module02.txt'), 'r') as f:
            module02_txt = f.read()
        f.close()
        self.assertEqual(
            'Hello from module 1!' + '\n' + 'Hello from module 2!', module02_txt
        )

        # ************************************************* #
        # Execute module 4 (with and without `all-upstream` #
        # ************************************************* #

        # Expectation: module 4 depends on module 3. However, the output of module 3 is
        # not stored in a target. Therefore, running module 4 without including
        # 'all-upstream' should cause an error.

        # -------------------------------------
        # Execute command without `all-upstream`
        args = ['run', '--modules', 'module04.py']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules({'module04.py': 'ERROR'}) + \
            _run_task_end_events('PrismExceptionErrorEvent')
        self.assertEqual(' | '.join(expected_events), runtask_run_results)

        # -----------------------------------
        # Execute command with `all-upstream`
        self._remove_compiled_dir(wkdir)
        self._remove_files_in_output(wkdir)
        args = ['run', '--modules', 'module04.py', '--all-upstream']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        self.assertEqual(
            ' | '.join(simple_project_no_null_all_modules_expected_events),
            runtask_run_results
        )

        # Check the results of the output directory
        self.assertTrue(Path(wkdir / 'output' / 'module01.txt').is_file())
        self.assertTrue(Path(wkdir / 'output' / 'module02.txt').is_file())
        module02_txt = self._file_as_str(Path(wkdir / 'output' / 'module02.txt'))
        self.assertEqual(
            'Hello from module 1!' + '\n' + 'Hello from module 2!', module02_txt
        )

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_project_nested_module_dirs(self):
        """
        `prism run` in a project with directories in the modules folder
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '010_project_nested_module_dirs'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Helper function
        def check_modules_1_2_results():
            """
            Helper function to check the results of running modules 1 and 2. We will use
            this a couple of times.
            """
            # Check that .compiled directory is formed
            self.assertTrue(Path(wkdir / '.compiled').is_dir())
            self.assertTrue(Path(wkdir / '.compiled' / 'manifest.json').is_file())

            # Check that outputs are created
            self.assertTrue(Path(wkdir / 'output' / 'module01.txt').is_file())
            self.assertTrue(Path(wkdir / 'output' / 'module02.txt').is_file())
            with open(Path(wkdir / 'output' / 'module02.txt'), 'r') as f:
                module02_txt = f.read()
            f.close()
            self.assertEqual(
                'Hello from module 1!' + '\n' + 'Hello from module 2!',
                module02_txt
            )

        # ****************************************************** #
        # Execute all modules in extract folder using '*' syntax #
        # ****************************************************** #

        args = ['run', '--modules', 'extract/*']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(
                {
                    'extract/module01.py': 'DONE',
                    'extract/module02.py': 'DONE'
                }) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check manifest
        manifest = self._load_manifest(Path(wkdir / '.compiled' / 'manifest.json'))
        extract_module01_refs = self._load_module_refs("extract/module01.py", manifest)
        extract_module02_refs = self._load_module_refs("extract/module02.py", manifest)
        load_module03_refs = self._load_module_refs("load/module03.py", manifest)
        module04_refs = self._load_module_refs("module04.py", manifest)
        self.assertEqual([], extract_module01_refs)
        self.assertEqual("extract/module01.py", extract_module02_refs)
        self.assertEqual("extract/module02.py", load_module03_refs)
        self.assertEqual("load/module03.py", module04_refs)

        # Check results
        check_modules_1_2_results()

        # Remove all files in the compiled and output directory
        self._remove_compiled_dir(wkdir)
        self._remove_files_in_output(wkdir)

        # ***************************************************************** #
        # Execute all modules in extract /load folder using explicit syntax #
        # ***************************************************************** #

        args = [
            'run',
            '--modules',
            'extract/module01.py',
            'extract/module02.py',
            'load/module03.py'
        ]
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(
                {
                    'extract/module01.py': 'DONE',
                    'extract/module02.py': 'DONE',
                    'load/module03.py': 'DONE',
                }) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check results
        check_modules_1_2_results()

        # Remove all files in the compiled and output directory
        self._remove_compiled_dir(wkdir)
        self._remove_files_in_output(wkdir)

        # ******************* #
        # Execute all modules #
        # ******************* #

        args = ['run']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(
                {
                    'extract/module01.py': 'DONE',
                    'extract/module02.py': 'DONE',
                    'load/module03.py': 'DONE',
                    'module04.py': 'DONE'
                }) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check output of modules 1 and 2
        check_modules_1_2_results()

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_bad_task_ref(self):
        """
        `prism run` fails in a project with a bad mod ref
        """
        self.maxDiff = None
        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '011_bad_task_ref'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        if Path(wkdir / '.compiled').is_dir():
            shutil.rmtree(Path(wkdir / '.compiled'))

        args = ['run']
        run_run = self._run_prism(args)
        run_run_results = run_run.get_results()
        expected_events = [
            'SeparatorEvent',
            'TaskRunEvent',
            'CurrentProjectDirEvent',
            'EmptyLineEvent',
            'ExecutionEvent - parsing prism_project.py - RUN',
            'ExecutionEvent - parsing prism_project.py - DONE',
            'ExecutionEvent - module DAG - RUN',
            'ExecutionEvent - module DAG - ERROR',
        ] + _run_task_end_events('PrismExceptionErrorEvent')
        self.assertEqual(' | '.join(expected_events), run_run_results)

        # The .compiled directory will be created
        self.assertTrue(Path(wkdir / '.compiled').is_dir())

        # But, the manifest file will not be
        self.assertFalse(Path(wkdir / '.compiled' / 'manifest.json').is_file())

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_concurrency(self):
        """
        Test concurrent behavior when threads>1
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '012_concurrency'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        if Path(wkdir / '.compiled').is_dir():
            shutil.rmtree(Path(wkdir / '.compiled'))
        self.maxDiff = None
        args = ['run']
        self._run_prism(args)

        # Get times
        module2_times = pd.read_csv(wkdir / 'output' / 'module02.csv')
        module1_times = pd.read_csv(wkdir / 'output' / 'module01.csv')

        # Module 1 and 2 should start at the same time
        module2_start_time = int(module2_times['start_time'][0])
        module1_start_time = int(module1_times['start_time'][0])
        self.assertTrue(abs(module2_start_time - module1_start_time) <= 1)

        # Module 2 should finish before module 1
        module2_end_time = int(module2_times['end_time'][0])
        module1_end_time = int(module1_times['end_time'][0])
        self.assertTrue(module2_end_time < module1_end_time)
        self.assertTrue(abs(10 - (module1_end_time - module2_end_time)) <= 1)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove stuff in output to avoid recommitting to github
        self._remove_files_in_output(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_user_context_cli(self):
        """
        Test that CLI user context works as expected
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '005_simple_project_no_null'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        if Path(wkdir / '.compiled').is_dir():
            shutil.rmtree(Path(wkdir / '.compiled'))
        self.maxDiff = None

        # Remove files in output folder
        self._remove_files_in_output(wkdir)

        # New output path
        output_path = str(wkdir.parent)
        self.assertFalse((Path(output_path) / 'module01.txt').is_file())
        args = ['run', '--modules', 'module01.py', '--vars', f'OUTPUT={output_path}']
        self._run_prism(args)

        # Get output
        self.assertTrue((Path(output_path) / 'module01.txt').is_file())
        module01_txt = self._file_as_str(Path(output_path) / 'module01.txt')
        self.assertEqual('Hello from module 1!', module01_txt)
        os.unlink(Path(output_path) / 'module01.txt')

        # Re-run to place output in normal directory
        args = ['run']
        self._run_prism(args)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_all_downstream(self):
        """
        Test that `all-downstream` argument functions as expected
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '005_simple_project_no_null'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run', '--modules', 'module01.py', '--all-downstream']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(
                {
                    'module01.py': 'DONE',
                    'module02.py': 'DONE',
                    'module03.py': 'DONE',
                    'module04.py': 'DONE',
                }) + \
            _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check manifest
        self.assertTrue(Path(wkdir / '.compiled').is_dir())
        self.assertTrue(Path(wkdir / '.compiled' / 'manifest.json').is_file())
        manifest = self._load_manifest(Path(wkdir / '.compiled' / 'manifest.json'))
        module01_refs = self._load_module_refs("module01.py", manifest)
        module02_refs = self._load_module_refs("module02.py", manifest)
        module03_refs = self._load_module_refs("module03.py", manifest)
        module04_refs = self._load_module_refs("module04.py", manifest)
        self.assertEqual([], module01_refs)
        self.assertEqual("module01.py", module02_refs)
        self.assertEqual("module02.py", module03_refs)
        self.assertEqual("module03.py", module04_refs)

        # Check that outputs are created
        self.assertTrue(Path(wkdir / 'output' / 'module01.txt').is_file())
        self.assertTrue(Path(wkdir / 'output' / 'module02.txt').is_file())
        with open(Path(wkdir / 'output' / 'module02.txt'), 'r') as f:
            module02_txt = f.read()
        f.close()
        self.assertEqual(
            'Hello from module 1!' + '\n' + 'Hello from module 2!',
            module02_txt
        )

        # Remove all files in the compiled directory
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def _check_trigger_output(self, wkdir: Path):
        """
        Our test trigger function outputs a .txt file to the wkdir / 'output' folder.
        Check that this exists.
        """
        self.assertTrue(Path(wkdir / '.compiled').is_dir())
        self.assertTrue(Path(wkdir / 'output' / 'trigger.txt').is_file())
        with open(Path(wkdir / 'output' / 'trigger.txt'), 'r') as f:
            trigger_txt = f.read()
        self.assertEqual('This is outputted from the trigger function!', trigger_txt)

    def _check_trigger_events(self,
        execution_event_dict: Dict[str, str],
        circa_trigger_header_event: List[str] = ['TriggersHeaderEvent'],
        final_status: str = "DONE"
    ):
        """
        Triggers kick of a predictable set of events. Check that these exist.
        """
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(execution_event_dict) + \
            ["EmptyLineEvent"] + \
            circa_trigger_header_event + \
            [
                "ExecutionEvent - test_trigger_function - RUN",  # noqa: E501
                f"ExecutionEvent - test_trigger_function - {final_status}",  # noqa: E501
            ]
        return expected_events

    def test_trigger_on_success(self):
        """
        Test on_success trigger
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '014_test_triggers_normal'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run', '--modules', 'module01.py']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module01.py': 'DONE'}
        ) + _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check manifest / output
        self._check_trigger_output(wkdir)

        # Remove all files in the compiled directory
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_trigger_on_failure(self):
        """
        Test on_failure trigger
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '014_test_triggers_normal'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run', '--modules', 'module02.py']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module02.py': 'ERROR'},
            ["ExecutionErrorEvent", "TriggersHeaderEvent"]
        ) + ["SeparatorEvent"]
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check manifest / output
        self._check_trigger_output(wkdir)

        # Remove all files in the compiled directory
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_trigger_no_directory(self):
        """
        Test trigger function when there is no `TRIGGERS_YML_PATH` in prism_project.py
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '015_test_triggers_no_dir'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run', '--modules', 'module01.py']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module01.py': 'DONE'},
            ["TriggersHeaderEvent", "TriggersPathNotDefined"]
        ) + _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check that manifest was created
        self._check_trigger_output(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_bad_trigger(self):
        """
        Test trigger function with a bad trigger
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '016_test_triggers_error'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module01.py': 'DONE'},
            ["TriggersHeaderEvent"],
            'ERROR'
        ) + ['EmptyLineEvent', 'ExecutionErrorEvent', 'SeparatorEvent']
        self.assertEqual(' | '.join(expected_events), run_results)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_triggers_with_extra_key(self):
        """
        An extra key in `triggers.yml` should raise a warning
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '017_test_triggers_extra_key'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module01.py': 'DONE'},
            ["TriggersHeaderEvent", "UnexpectedTriggersYmlKeysEvent"]
        ) + _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), run_results)

        # Check that manifest was created
        self._check_trigger_output(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_triggers_no_include(self):
        """
        A trigger function in an external module/package without an accompanying
        `include` path will throw an error.
        """

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '018_test_triggers_no_include'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run all modules downstream of module01.py
        args = ['run']
        run = self._run_prism(args)
        run_results = run.get_results()
        expected_events = self._check_trigger_events(
            {'module01.py': 'DONE'},
            ["TriggersHeaderEvent"],
            'ERROR'
        ) + ['EmptyLineEvent', 'ExecutionErrorEvent', 'SeparatorEvent']
        self.assertEqual(' | '.join(expected_events), run_results)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up wkdir for the next test case
        self._set_up_wkdir()

    def test_decorator_tasks_with_targets(self):
        """
        `prism run` on a project where all the tasks are functions decorated with
        `@task`
        """
        self.maxDiff = None

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '019_dec_targets'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run
        args = ['run']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        expected_events = self._check_trigger_events(
            {
                'extract.py': 'DONE',
                'load.py': 'DONE'
            },
        ) + _run_task_end_events('TaskSuccessfulEndEvent')
        self.assertEqual(' | '.join(expected_events), runtask_run_results)

        # Check output of 'extract' task
        self.assertTrue(Path(wkdir / 'output' / 'astros.json').is_file())
        self.assertTrue(Path(wkdir / 'output' / 'second_target.txt').is_file())

        # Astros JSON file
        with open(Path(wkdir / 'output' / 'astros.json'), 'r') as f:
            astros_str = f.read()
        astros_dict = json.loads(astros_str)
        self.assertEqual(astros_dict["message"], "success")

        # Dummy second target text file
        with open(Path(wkdir / 'output' / 'second_target.txt'), 'r') as f:
            second_target = f.read()
        self.assertEqual(second_target, "second target")

        # Check output of 'load' task
        names = [
            "Andrey Fedyaev",
            "Deng Qingming",
            "Dmitry Petelin",
            "Fei Junlong",
            "Frank Rubio",
            "Sergey Prokopyev",
            "Stephen Bowen",
            "Sultan Alneyadi",
            "Warren Hoburg",
            "Zhang Lu",
        ]
        for n in names:
            formatted_name = n.lower().replace(" ", "_")
            self.assertTrue(Path(wkdir / 'output' / f'{formatted_name}.txt').is_file())
            with open(Path(wkdir / 'output' / f'{formatted_name}.txt'), 'r') as f:
                contents = f.read()
            self.assertEqual(contents, n)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up the working directory
        self._set_up_wkdir()

    def test_decorator_tasks_with_retries(self):
        """
        `prism run` on a project where all the tasks are functions decorated with
        `@task` and the user wants to retry a task
        """
        self.maxDiff = None

        # Set working directory
        wkdir = Path(TEST_PROJECTS) / '020_dec_retries'
        os.chdir(wkdir)

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Remove all files in the output directory
        self._remove_files_in_output(wkdir)

        # Run
        args = ['run']
        runtask_run = self._run_prism(args)
        runtask_run_results = runtask_run.get_results()
        expected_events = run_success_starting_events + \
            ['TasksHeaderEvent'] + \
            _execution_events_modules(
                {
                    'extract.py': 'DONE',
                    'load.py': 'ERROR'
                },
            ) + \
            ['DelayEvent'] + \
            _execution_events_modules(
                {'load.py (RETRY 1)': 'ERROR'}
            ) + \
            [
                "EmptyLineEvent",
                "ExecutionErrorEvent",
                "TriggersHeaderEvent",
                "ExecutionEvent - test_trigger_function - RUN",
                "ExecutionEvent - test_trigger_function - DONE",
                "SeparatorEvent"
            ]
        self.assertEqual(' | '.join(expected_events), runtask_run_results)

        # Check output of 'extract' task
        self.assertTrue(Path(wkdir / 'output' / 'astros.json').is_file())
        with open(Path(wkdir / 'output' / 'astros.json'), 'r') as f:
            astros_str = f.read()
        astros_dict = json.loads(astros_str)
        self.assertEqual(astros_dict["message"], "success")

        # Output of 'load' task was not created
        names = [
            "Andrey Fedyaev",
            "Deng Qingming",
            "Dmitry Petelin",
            "Fei Junlong",
            "Frank Rubio",
            "Sergey Prokopyev",
            "Stephen Bowen",
            "Sultan Alneyadi",
            "Warren Hoburg",
            "Zhang Lu",
        ]
        for n in names:
            formatted_name = n.lower().replace(" ", "_")
            self.assertFalse(Path(wkdir / 'output' / f'{formatted_name}.txt').is_file())

        # Remove the .compiled directory, if it exists
        self._remove_compiled_dir(wkdir)

        # Set up the working directory
        self._set_up_wkdir()
