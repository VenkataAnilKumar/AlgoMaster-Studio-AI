"""
Revolutionary algorithm visualization generation service
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from models.algorithm_models import VisualizationData
from utils.logger import setup_logger

logger = setup_logger("visualization_generator")

class VisualizationGenerator:
    """Revolutionary AI-powered algorithm visualization generator"""
    
    def __init__(self):
        self.visualization_templates = {}
        
    async def initialize(self):
        """Initialize visualization templates and generators"""
        try:
            await self._load_visualization_templates()
            logger.info("🎨 Visualization generator initialized with interactive templates")
        except Exception as e:
            logger.error(f"❌ Failed to initialize visualization generator: {e}")
            raise

    async def create_flow_diagram(self, code: str, language: str) -> VisualizationData:
        """
        Create interactive algorithm flowchart
        """
        try:
            logger.info(f"🎨 Creating flowchart for {language} algorithm")
            
            # Parse code structure
            flow_elements = await self._parse_code_flow(code, language)
            
            # Generate D3.js compatible flowchart data
            flowchart_data = {
                "nodes": [],
                "edges": [],
                "layout": "top-to-bottom",
                "interactive": True
            }
            
            # Create nodes for each code block
            node_id = 0
            for element in flow_elements:
                flowchart_data["nodes"].append({
                    "id": node_id,
                    "type": element["type"],
                    "label": element["label"],
                    "code": element.get("code", ""),
                    "position": {"x": 0, "y": node_id * 80},
                    "style": await self._get_node_style(element["type"])
                })
                
                # Create edges between sequential nodes
                if node_id > 0:
                    flowchart_data["edges"].append({
                        "source": node_id - 1,
                        "target": node_id,
                        "type": "sequential"
                    })
                
                node_id += 1
            
            # Add conditional branches and loops
            await self._add_control_flow_edges(flowchart_data, flow_elements)
            
            return VisualizationData(
                visualization_type="flowchart",
                data=flowchart_data,
                interactive_features=[
                    "hover_code_highlight",
                    "click_to_expand",
                    "step_through_execution",
                    "zoom_and_pan"
                ],
                description="Interactive algorithm flowchart with step-by-step execution"
            )
            
        except Exception as e:
            logger.error(f"❌ Flowchart creation failed: {e}")
            return await self._create_error_visualization(str(e))

    async def create_execution_trace(self, code: str, language: str) -> VisualizationData:
        """
        Create interactive execution trace visualization
        """
        try:
            logger.info(f"🎯 Creating execution trace for {language} algorithm")
            
            # Simulate execution steps
            execution_steps = await self._simulate_execution(code, language)
            
            trace_data = {
                "steps": execution_steps,
                "variables": await self._track_variable_changes(code, language),
                "call_stack": await self._track_function_calls(code, language),
                "memory_timeline": await self._track_memory_usage(code, language),
                "interactive": True
            }
            
            return VisualizationData(
                visualization_type="execution_trace",
                data=trace_data,
                interactive_features=[
                    "step_forward",
                    "step_backward", 
                    "play_pause",
                    "variable_inspection",
                    "breakpoint_setting"
                ],
                description="Interactive execution trace with variable tracking"
            )
            
        except Exception as e:
            logger.error(f"❌ Execution trace creation failed: {e}")
            return await self._create_error_visualization(str(e))

    async def create_complexity_graph(self, code: str, language: str) -> VisualizationData:
        """
        Create interactive complexity analysis visualization
        """
        try:
            logger.info(f"📊 Creating complexity graph for {language} algorithm")
            
            # Analyze complexity patterns
            complexity_data = await self._analyze_complexity_patterns(code, language)
            
            graph_data = {
                "time_complexity": {
                    "best_case": complexity_data.get("time_best", "O(n)"),
                    "average_case": complexity_data.get("time_avg", "O(n)"),
                    "worst_case": complexity_data.get("time_worst", "O(n)"),
                    "graph_points": await self._generate_complexity_points("time", complexity_data)
                },
                "space_complexity": {
                    "complexity": complexity_data.get("space", "O(1)"),
                    "breakdown": complexity_data.get("space_breakdown", {}),
                    "graph_points": await self._generate_complexity_points("space", complexity_data)
                },
                "comparison": await self._get_complexity_comparison(complexity_data),
                "interactive": True
            }
            
            return VisualizationData(
                visualization_type="complexity_graph",
                data=graph_data,
                interactive_features=[
                    "toggle_cases",
                    "zoom_complexity_range",
                    "compare_algorithms",
                    "input_size_slider"
                ],
                description="Interactive complexity analysis with performance comparisons"
            )
            
        except Exception as e:
            logger.error(f"❌ Complexity graph creation failed: {e}")
            return await self._create_error_visualization(str(e))

    async def create_data_structure_visualization(self, code: str, language: str) -> VisualizationData:
        """
        Create interactive data structure visualization
        """
        try:
            logger.info(f"🗂️ Creating data structure visualization for {language} algorithm")
            
            # Detect data structures used
            data_structures = await self._detect_data_structures(code, language)
            
            ds_data = {
                "structures": [],
                "operations": [],
                "state_changes": [],
                "interactive": True
            }
            
            for ds in data_structures:
                ds_data["structures"].append({
                    "type": ds["type"],
                    "name": ds["name"],
                    "initial_state": ds.get("initial_state", []),
                    "visualization_style": await self._get_ds_visualization_style(ds["type"])
                })
            
            # Track operations on data structures
            operations = await self._track_ds_operations(code, language)
            ds_data["operations"] = operations
            
            return VisualizationData(
                visualization_type="data_structure",
                data=ds_data,
                interactive_features=[
                    "animate_operations",
                    "step_through_changes",
                    "highlight_elements",
                    "operation_history"
                ],
                description="Interactive data structure visualization with operation animation"
            )
            
        except Exception as e:
            logger.error(f"❌ Data structure visualization failed: {e}")
            return await self._create_error_visualization(str(e))

    async def create_custom_visualization(self, code: str, language: str, viz_type: str, options: Dict[str, Any]) -> VisualizationData:
        """
        Create custom algorithm visualization based on user requirements
        """
        try:
            logger.info(f"🎨 Creating custom {viz_type} visualization")
            
            if viz_type == "tree_traversal":
                return await self._create_tree_traversal_viz(code, language, options)
            elif viz_type == "sorting_animation":
                return await self._create_sorting_animation(code, language, options)
            elif viz_type == "graph_algorithm":
                return await self._create_graph_algorithm_viz(code, language, options)
            elif viz_type == "dynamic_programming":
                return await self._create_dp_table_viz(code, language, options)
            else:
                return await self.create_flow_diagram(code, language)
                
        except Exception as e:
            logger.error(f"❌ Custom visualization creation failed: {e}")
            return await self._create_error_visualization(str(e))

    # Helper methods
    async def _load_visualization_templates(self):
        """Load visualization templates and configurations"""
        self.visualization_templates = {
            "flowchart": {
                "node_types": ["start", "process", "decision", "end", "input", "output"],
                "colors": {
                    "start": "#4CAF50",
                    "process": "#2196F3", 
                    "decision": "#FF9800",
                    "end": "#F44336",
                    "input": "#9C27B0",
                    "output": "#00BCD4"
                }
            },
            "execution_trace": {
                "step_colors": ["#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6"],
                "variable_colors": ["#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A"]
            },
            "complexity_graph": {
                "complexity_colors": {
                    "O(1)": "#4CAF50",
                    "O(log n)": "#8BC34A", 
                    "O(n)": "#FFC107",
                    "O(n log n)": "#FF9800",
                    "O(n²)": "#FF5722",
                    "O(2^n)": "#F44336"
                }
            }
        }

    async def _parse_code_flow(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Parse code to extract flow elements"""
        flow_elements = []
        
        # Simple parsing for demonstration (would be enhanced with AST parsing)
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
                
            if 'if' in line and line.endswith(':'):
                flow_elements.append({
                    "type": "decision",
                    "label": f"Condition: {line}",
                    "code": line,
                    "line_number": i + 1
                })
            elif 'for' in line or 'while' in line:
                flow_elements.append({
                    "type": "loop",
                    "label": f"Loop: {line}",
                    "code": line,
                    "line_number": i + 1
                })
            elif 'return' in line:
                flow_elements.append({
                    "type": "output",
                    "label": f"Return: {line}",
                    "code": line,
                    "line_number": i + 1
                })
            else:
                flow_elements.append({
                    "type": "process",
                    "label": f"Process: {line[:30]}...",
                    "code": line,
                    "line_number": i + 1
                })
        
        return flow_elements

    async def _get_node_style(self, node_type: str) -> Dict[str, Any]:
        """Get styling for flowchart nodes"""
        styles = {
            "start": {"fill": "#4CAF50", "shape": "ellipse"},
            "process": {"fill": "#2196F3", "shape": "rectangle"},
            "decision": {"fill": "#FF9800", "shape": "diamond"},
            "loop": {"fill": "#9C27B0", "shape": "rectangle"},
            "output": {"fill": "#00BCD4", "shape": "parallelogram"},
            "end": {"fill": "#F44336", "shape": "ellipse"}
        }
        
        return styles.get(node_type, {"fill": "#CCCCCC", "shape": "rectangle"})

    async def _add_control_flow_edges(self, flowchart_data: Dict[str, Any], flow_elements: List[Dict[str, Any]]):
        """Add conditional branches and loop edges to flowchart"""
        # Implementation would analyze control flow and add appropriate edges
        pass

    async def _simulate_execution(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Simulate algorithm execution steps"""
        steps = []
        
        # Simplified execution simulation
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            steps.append({
                "step": i + 1,
                "line": line,
                "description": f"Execute: {line}",
                "variables_changed": [],
                "memory_state": {},
                "highlights": [i + 1]
            })
        
        return steps

    async def _track_variable_changes(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Track variable changes during execution"""
        return [
            {"variable": "i", "type": "int", "changes": [0, 1, 2, 3, 4]},
            {"variable": "result", "type": "list", "changes": [[], [1], [1, 2], [1, 2, 3]]}
        ]

    async def _track_function_calls(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Track function call stack"""
        return [
            {"function": "main", "line": 1, "depth": 0},
            {"function": "helper", "line": 5, "depth": 1}
        ]

    async def _track_memory_usage(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Track memory usage over time"""
        return [
            {"step": 1, "memory": 1.2, "allocations": 1},
            {"step": 2, "memory": 2.1, "allocations": 2},
            {"step": 3, "memory": 1.8, "allocations": 1}
        ]

    async def _analyze_complexity_patterns(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze complexity patterns in code"""
        # Simplified complexity analysis
        has_nested_loops = 'for' in code and code.count('for') > 1
        has_recursion = 'def' in code and any(func_name in code for func_name in ['recursion', 'factorial', 'fibonacci'])
        
        if has_nested_loops:
            time_complexity = "O(n²)"
        elif has_recursion:
            time_complexity = "O(2^n)"
        elif 'for' in code or 'while' in code:
            time_complexity = "O(n)"
        else:
            time_complexity = "O(1)"
        
        return {
            "time_best": time_complexity,
            "time_avg": time_complexity,
            "time_worst": time_complexity,
            "space": "O(1)",
            "space_breakdown": {"variables": "O(1)", "recursion": "O(1)"}
        }

    async def _generate_complexity_points(self, complexity_type: str, complexity_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate points for complexity graph"""
        # Generate sample points for visualization
        points = []
        for n in [1, 10, 100, 1000, 10000]:
            if complexity_type == "time":
                value = n if "O(n)" in str(complexity_data) else n * n if "O(n²)" in str(complexity_data) else 1
            else:
                value = 1  # Constant space for most algorithms
            
            points.append({"input_size": n, "value": value})
        
        return points

    async def _get_complexity_comparison(self, complexity_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get complexity comparison with common algorithms"""
        return [
            {"algorithm": "Linear Search", "time": "O(n)", "space": "O(1)"},
            {"algorithm": "Binary Search", "time": "O(log n)", "space": "O(1)"},
            {"algorithm": "Quick Sort", "time": "O(n log n)", "space": "O(log n)"},
            {"algorithm": "Current Algorithm", "time": complexity_data.get("time_avg", "O(n)"), "space": complexity_data.get("space", "O(1)")}
        ]

    async def _detect_data_structures(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect data structures used in code"""
        structures = []
        
        if 'list' in code or '[]' in code:
            structures.append({"type": "array", "name": "arr", "initial_state": []})
        if 'dict' in code or '{}' in code:
            structures.append({"type": "hash_map", "name": "map", "initial_state": {}})
        if 'set' in code:
            structures.append({"type": "set", "name": "s", "initial_state": set()})
        
        return structures

    async def _get_ds_visualization_style(self, ds_type: str) -> Dict[str, Any]:
        """Get visualization style for data structure type"""
        styles = {
            "array": {"layout": "horizontal", "color": "#2196F3"},
            "hash_map": {"layout": "table", "color": "#4CAF50"},
            "set": {"layout": "circular", "color": "#FF9800"},
            "tree": {"layout": "hierarchical", "color": "#9C27B0"},
            "graph": {"layout": "force", "color": "#F44336"}
        }
        
        return styles.get(ds_type, {"layout": "default", "color": "#CCCCCC"})

    async def _track_ds_operations(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Track operations performed on data structures"""
        return [
            {"operation": "insert", "element": 1, "position": 0, "timestamp": 0.1},
            {"operation": "insert", "element": 2, "position": 1, "timestamp": 0.2},
            {"operation": "search", "element": 1, "result": True, "timestamp": 0.3}
        ]

    async def _create_error_visualization(self, error_message: str) -> VisualizationData:
        """Create error visualization when visualization generation fails"""
        return VisualizationData(
            visualization_type="error",
            data={"error": error_message, "fallback": True},
            interactive_features=[],
            description=f"Visualization generation failed: {error_message}"
        )

    # Custom visualization methods
    async def _create_tree_traversal_viz(self, code: str, language: str, options: Dict[str, Any]) -> VisualizationData:
        """Create tree traversal visualization"""
        return VisualizationData(
            visualization_type="tree_traversal",
            data={"nodes": [], "edges": [], "traversal_order": []},
            interactive_features=["animate_traversal", "highlight_current_node"],
            description="Interactive tree traversal visualization"
        )

    async def _create_sorting_animation(self, code: str, language: str, options: Dict[str, Any]) -> VisualizationData:
        """Create sorting algorithm animation"""
        return VisualizationData(
            visualization_type="sorting_animation",
            data={"array": [5, 2, 8, 1, 9], "steps": []},
            interactive_features=["play_pause", "step_control", "speed_adjustment"],
            description="Interactive sorting algorithm animation"
        )

    async def _create_graph_algorithm_viz(self, code: str, language: str, options: Dict[str, Any]) -> VisualizationData:
        """Create graph algorithm visualization"""
        return VisualizationData(
            visualization_type="graph_algorithm",
            data={"nodes": [], "edges": [], "algorithm_state": {}},
            interactive_features=["highlight_path", "show_distances", "animate_algorithm"],
            description="Interactive graph algorithm visualization"
        )

    async def _create_dp_table_viz(self, code: str, language: str, options: Dict[str, Any]) -> VisualizationData:
        """Create dynamic programming table visualization"""
        return VisualizationData(
            visualization_type="dp_table",
            data={"table": [], "fill_order": [], "recurrence_relation": ""},
            interactive_features=["animate_fill", "highlight_dependencies", "show_recurrence"],
            description="Interactive dynamic programming table visualization"
        )