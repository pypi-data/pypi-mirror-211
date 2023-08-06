"""
DagCompiler and CompiledDag classes

Table of Contents
- Imports
- Class definition
"""

###########
# Imports #
###########

# Standard library imports
import os
import networkx as nx
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Prism-specific imports
import prism.constants
import prism.exceptions
import prism.logging
import prism.parsers.ast_parser as ast_parser
import prism.infra.module
from prism.infra.manifest import Manifest, ModuleManifest
from prism.infra.project import PrismProject


####################
# Class definition #
####################

class CompiledDag:
    """
    Compiled DAG
    """
    def __init__(self,
        modules_dir: Path,
        nxdag: nx.DiGraph,
        topological_sort: List[Path],
        user_arg_modules: List[Path],
        module_manifests: Dict[Path, ModuleManifest]
    ):
        self.modules_dir = modules_dir
        self.nxdag = nxdag
        self.topological_sort = topological_sort
        self.user_arg_modules = user_arg_modules
        self.module_manifests = module_manifests

        # Store full paths in attribute
        self.topological_sort_full_path = [
            self.modules_dir / module for module in self.topological_sort
        ]

        # Create module objects
        self.compiled_modules = []
        for relative, full in zip(self.topological_sort, self.topological_sort_full_path):  # noqa: E501
            self.compiled_modules.append(
                prism.infra.module.CompiledModule(
                    relative, full, self.module_manifests[relative]
                )
            )


class DagCompiler:
    """
    Class for parsing mod refs, building DAG
    """

    def __init__(self,
        project_dir: Path,
        compiled_dir: Path,
        all_modules: List[Path],
        user_arg_modules: List[Path],
        user_arg_all_downstream: bool,
        project: Optional[PrismProject] = None
    ):
        self.project_dir = project_dir
        self.compiled_dir = compiled_dir
        self.all_modules = all_modules
        self.user_arg_modules = user_arg_modules
        self.project = project
        os.chdir(project_dir)

        # Modules can only be executed if their predecessors are explicitly run or have
        # targets. For example, if our DAG is A --> B --> C and we call `prism run
        # --modules C`, then Prism will parse the execution order, instantiate but NOT
        # execute tasks A and B, and then run task C. In other words, A and B will
        # always be instantiated; the --all-upstream argument controls whether A and B
        # are executed.

        # This is why we don't need to keep track of the --all-upstream argument; it
        # doesn't affect what our topological sort looks like. However, the
        # --all-downstream argument does, since successors do not need to be
        # instantiated at all.
        self.user_arg_all_downstream = user_arg_all_downstream

        # Path of modules
        self.modules_dir = self.project_dir / 'modules'

        # Module manifests
        self.module_manifests: Dict[Path, ModuleManifest] = {}

    def parse_task_refs(self,
        modules: List[Path],
        parent_path: Path
    ) -> Dict[Path, Any]:
        """
        Parse node dictionary listed at the beginning of each python script. If
        node_dict does not exist in any script, throw an error.

        args:
            modules: modules to compile
            parent_path: parent path of modules
        returns:
            module references as a dictionary
        """

        # This is only ever called on the output of `get_all_modules`, which sorts the
        # modules alphabetically. Therefore, all mod refs will be sorted.
        task_refs_dict: Dict[Path, Any] = {}
        for m in modules:
            parser = ast_parser.AstParser(m, parent_path)
            task_refs = parser.parse()
            if task_refs is None or task_refs == '' or task_refs == []:
                task_refs_dict[m] = None
            else:
                task_refs_dict[m] = task_refs

            # Keep track of module manifest
            self.module_manifests[m] = parser.module_manifest

        return task_refs_dict

    def add_graph_elem(self,
        elem: Any,
        master: List[Any]
    ) -> List[Any]:
        """
        Add graph element `elem` to master list of elements

        args:
            elem: graph element to add (either a node or an edge)
            master: master list of elements (either nodes or edges)
        returns
            master list of elements with new elem
        """
        if elem not in master:
            master += [elem]  # type: ignore
        else:
            return master
        return master

    def add_graph_node(self,
        elem: Path,
        master: List[Path]
    ) -> List[Path]:
        """
        To resolve mypy errors...
        """
        return self.add_graph_elem(elem, master)

    def add_graph_edge(self,
        elem: Tuple[Path, Path],
        master: List[Tuple[Path, Path]]
    ) -> List[Tuple[Path, Path]]:
        """
        To resolve mypy errors...
        """
        return self.add_graph_elem(elem, master)

    def create_nodes_edges(self,
        module_references: Dict[Path, Any]
    ) -> Tuple[List[Path], List[Tuple[Path, Path]]]:
        """
        Create nodes / edges from module connections

        args:
            module_references: connections defined via {{ mod(...) }} in modules
        outputs:
            nodes: list of nodes (modules)
            edges: list of edges (tuple of nodes, i.e. modules)
        """

        # Create edges and nodes
        edges: List[Tuple[Path, Path]] = []
        nodes: List[Path] = []

        # Iterate through module references. Keys represent distinct modules in the DAG,
        # and values represent the modules that feed into the key.
        for mod, ref in module_references.items():
            nodes = self.add_graph_node(mod, nodes)
            if ref is None:
                pass
            elif isinstance(ref, Path):
                nodes = self.add_graph_node(ref, nodes)
                edges = self.add_graph_edge((ref, mod), edges)
            else:
                for v in ref:
                    nodes = self.add_graph_node(v, nodes)
                    edges = self.add_graph_edge((v, mod), edges)
        return nodes, edges

    def create_dag(self,
        nodes: List[Path],
        edges: List[Tuple[Path, Path]]
    ) -> nx.DiGraph:
        """
        Create DAG from edges

        args:
            user_arg_modules: modules passed in user arguments
            nodes: list of nodes (modules)
            edges: list of edges (tuple of nodes, i.e. modules)
        outputs:
            topological sort of edges
        """
        # Instantiate graph
        graph = nx.DiGraph()

        # If there are no nodes in the DAG, then throw an error. This should never
        # happen.
        if len(nodes) == 0:
            raise prism.exceptions.RuntimeException(message='DAG has 0 nodes')

        # Add the edges/nodes
        graph.add_edges_from(edges)
        graph.add_nodes_from(nodes)

        # Check if graph is a DAG
        if not nx.is_directed_acyclic_graph(graph):
            all_scc = nx.algorithms.components.strongly_connected_components(graph)
            cycles = []
            for component in all_scc:
                component = set([str(elem) for elem in list(component)])
                if len(component) > 1:
                    cycles.append(component)
            raise prism.exceptions.DAGException(
                message=f"invalid DAG, cycle found in {str(cycles)}"
            )

        return graph

    def get_node_dependencies(self,
        graph: nx.DiGraph,
        start_nodes: List[Path]
    ) -> List[Path]:
        """
        Parse the DiGraph and get all nodes upstream of the `start_nodes`

        args:
            graph: DAG
            start_nodes: list of nodes for which to retrieve upstream dependencies
        returns:
            list of dependencies
        """
        # Add all start nodes to the list of dependencies with a depth of 0
        deps = [x for x in start_nodes]

        # Iterate through the start nodes and extract the predecessors
        for node in deps:
            for prenode in graph.predecessors(node):
                deps.append(prenode)

        # Get unique dependencies
        unique_deps = list(set(deps))
        return unique_deps

    def get_node_successors(self,
        graph: nx.DiGraph,
        start_nodes: List[Path]
    ) -> List[Path]:
        """
        Parse the DiGraph and get all nodes downstream of the `start_nodes`

        args:
            graph: DAG
            start_nodes: list of nodes for which to retrieve upstream dependencies
        returns:
            list of successors
        """
        # Add all start nodes to the list of successors with a depth of 0
        successors = [x for x in start_nodes]

        # Iterate through the start nodes and extract the predecessors
        for node in successors:
            for postnode in graph.successors(node):
                successors.append(postnode)

        # Get unique dependencies
        unique_successors = list(set(successors))
        return unique_successors

    def create_topsort(self,
        all_modules: List[Path],
        user_arg_modules: List[Path],
        parent_path: Path
    ) -> Any:
        """
        Parse mod refs, create the DAG, and create a topological sort of the DAG

        args:
            all_modules: list of all modules
            user_arg_modules: modules passed in user arguments
            parent_path: path containing the modules
            compiler_dict: globals dictionary for compiler
        returns:
            topological sorted DAG as a list
        """

        # Create a DAG using all the modules. We use `all_modules` instead of
        # `user_arg_modules`, because using `user_arg_modules` will only compile/run the
        # modules referenced in the modules themselves. For example, if we have a dag A
        # --> B --> C and wish to to only compile/run script C, then our code will only
        # run script B. This will throw an error, because script B relies on script A,
        # and we will need to instantiate the script A task for the script B task to
        # execute fully.
        task_refs = self.parse_task_refs(all_modules, parent_path)
        nodes, edges = self.create_nodes_edges(task_refs)
        dag = self.create_dag(nodes, edges)

        # If `user_arg_modules` is equivalent to `all_modules`, then create a
        # topological sorting of the full DAG. From the NetworkX documentation: A
        # topological sort is a nonunique permutation of the nodes of a directed graph
        # such that an edge from u to v implies that u appears before v in the
        # topological sort order. This ordering is valid only if the graph has no
        # directed cycles.
        if len(user_arg_modules) == len(all_modules):
            all_topological_sorts = nx.algorithms.dag.all_topological_sorts(dag)
            all_topological_sorts_list = next(all_topological_sorts)

        # Otherwise, the user has selected to run a subset of the modules. Identify all
        # modules upstream (and potentially downstream) of `user_arg_modules`.
        else:

            # Keep only the dependencies, and create a topological sort.
            all_nodes = self.get_node_dependencies(dag, user_arg_modules)

            # Add successors if the user wants them
            if self.user_arg_all_downstream:
                all_nodes.extend(self.get_node_successors(dag, user_arg_modules))

            subgraph = dag.subgraph(list(set(all_nodes)))
            all_topological_sorts = nx.algorithms.dag.all_topological_sorts(subgraph)  # noqa: E501
            all_topological_sorts_list = next(all_topological_sorts)

        # Add each module to manifest
        for elem in all_topological_sorts_list:

            # Raise error if node not in project
            if elem not in all_modules:
                raise prism.exceptions.CompileException(
                    message=f'module `{str(elem)}` not found in project'
                )

        return dag, all_topological_sorts_list

    def compile(self) -> CompiledDag:
        """
        Compile the DAG
        """
        nxdag, all_topological_sorts_list = self.create_topsort(
            self.all_modules, self.user_arg_modules, self.modules_dir
        )

        # Dump manifest
        manifest = Manifest(list(self.module_manifests.values()))

        # Add the prism project to the Manifest
        if self.project is not None:
            prism_project_py_str = self.project.prism_project_py_str
        else:
            prism_project = PrismProject(
                project_dir=self.project_dir,
                user_context={},
                which="compile",
                filename="prism_project.py"
            )
            prism_project_py_str = prism_project.prism_project_py_str
        manifest.add_prism_project(prism_project_py_str)
        manifest.json_dump(self.compiled_dir)

        # Return dag
        dag = CompiledDag(
            self.modules_dir,
            nxdag,
            all_topological_sorts_list,
            self.user_arg_modules,
            self.module_manifests
        )
        return dag
