"""
Pydantic models for AlgoMaster-Studio-AI AI Engine
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AlgorithmRequest(BaseModel):
    """Request model for algorithm analysis"""
    algorithm_name: str = Field(..., description="Name of the algorithm")
    code: str = Field(..., description="Algorithm code to analyze")
    language: str = Field(..., description="Programming language (python, cpp, java, javascript)")
    test_cases: Optional[List[Dict[str, Any]]] = Field(default=[], description="Test cases for benchmarking")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis requested")

class ComplexityAnalysis(BaseModel):
    """Complexity analysis results"""
    time_complexity: str = Field(..., description="Time complexity in Big O notation")
    space_complexity: str = Field(..., description="Space complexity in Big O notation")
    detailed_analysis: str = Field(..., description="Detailed AI analysis")
    ast_metrics: Dict[str, Any] = Field(..., description="Abstract syntax tree metrics")
    optimization_score: float = Field(..., description="Code optimization score (0-10)")

class QualityAssessment(BaseModel):
    """Code quality assessment results"""
    overall_score: float = Field(..., description="Overall quality score (0-10)")
    metrics: Dict[str, float] = Field(..., description="Individual quality metrics")
    insights: List[str] = Field(..., description="AI-generated quality insights")
    recommendations: List[str] = Field(..., description="Improvement recommendations")

class AIExplanation(BaseModel):
    """AI-generated algorithm explanation"""
    explanation: str = Field(..., description="Comprehensive algorithm explanation")
    difficulty_level: str = Field(..., description="Algorithm difficulty level")
    learning_objectives: List[str] = Field(..., description="Key learning objectives")
    interactive_elements: List[Dict[str, Any]] = Field(..., description="Interactive learning elements")
    prerequisite_concepts: List[str] = Field(..., description="Required prerequisite knowledge")
    follow_up_exercises: List[Dict[str, str]] = Field(..., description="Suggested follow-up exercises")

class OptimizationSuggestion(BaseModel):
    """Code optimization suggestion"""
    title: str = Field(..., description="Optimization title")
    description: str = Field(..., description="Detailed description")
    improvement: str = Field(..., description="Expected improvement")
    difficulty: str = Field(..., description="Implementation difficulty")
    implementation: str = Field(..., description="Code example")
    trade_offs: str = Field(..., description="Trade-offs to consider")

class BenchmarkResults(BaseModel):
    """Performance benchmark results"""
    execution_time: float = Field(..., description="Average execution time (ms)")
    memory_usage: float = Field(..., description="Peak memory usage (MB)")
    test_cases_passed: int = Field(..., description="Number of test cases passed")
    total_test_cases: int = Field(..., description="Total number of test cases")
    performance_score: float = Field(..., description="Performance score (0-10)")
    benchmark_details: List[Dict[str, Any]] = Field(..., description="Detailed benchmark results")

class VisualizationData(BaseModel):
    """Algorithm visualization data"""
    visualization_type: str = Field(..., description="Type of visualization")
    data: Dict[str, Any] = Field(..., description="Visualization data")
    interactive_features: List[str] = Field(..., description="Available interactive features")
    description: str = Field(..., description="Visualization description")

class AnalysisResponse(BaseModel):
    """Complete algorithm analysis response"""
    algorithm_name: str = Field(..., description="Name of the analyzed algorithm")
    language: str = Field(..., description="Programming language")
    complexity_analysis: ComplexityAnalysis = Field(..., description="Complexity analysis results")
    quality_assessment: QualityAssessment = Field(..., description="Quality assessment results")
    ai_explanation: AIExplanation = Field(..., description="AI-generated explanation")
    optimization_suggestions: List[OptimizationSuggestion] = Field(..., description="Optimization suggestions")
    benchmark_results: BenchmarkResults = Field(..., description="Performance benchmark results")
    visualization: VisualizationData = Field(..., description="Algorithm visualization")
    analysis_timestamp: str = Field(..., description="Analysis timestamp")

class LearningRecommendation(BaseModel):
    """AI-powered learning recommendation"""
    category: str = Field(..., description="Learning category")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    algorithms: List[str] = Field(..., description="Recommended algorithms")
    estimated_time: str = Field(..., description="Estimated learning time")
    ai_insight: str = Field(..., description="AI-generated insight")

class AlgorithmLibraryItem(BaseModel):
    """Algorithm library item"""
    name: str = Field(..., description="Algorithm name")
    difficulty: str = Field(..., description="Difficulty level")
    ai_insight: str = Field(..., description="AI-generated insight")
    category: str = Field(..., description="Algorithm category")
    implementation_languages: List[str] = Field(default=["cpp", "python", "java"], description="Available languages")

class SolutionRequest(BaseModel):
    """Request for AI solution generation"""
    problem_description: str = Field(..., description="Problem description")
    target_language: str = Field(..., description="Target programming language")
    difficulty_level: str = Field(default="medium", description="Difficulty level")
    constraints: Optional[List[str]] = Field(default=[], description="Problem constraints")
    examples: Optional[List[Dict[str, str]]] = Field(default=[], description="Example inputs/outputs")

class GeneratedSolution(BaseModel):
    """AI-generated solution"""
    solution_code: str = Field(..., description="Generated solution code")
    approach_explanation: str = Field(..., description="Algorithm approach explanation")
    complexity_analysis: Dict[str, str] = Field(..., description="Time and space complexity")
    test_cases: List[Dict[str, Any]] = Field(..., description="Generated test cases")
    alternative_approaches: List[str] = Field(..., description="Alternative solution approaches")
    learning_notes: List[str] = Field(..., description="Key learning insights")

class VisualizationRequest(BaseModel):
    """Request for algorithm visualization"""
    code: str = Field(..., description="Algorithm code")
    language: str = Field(..., description="Programming language")
    visualization_type: str = Field(default="flowchart", description="Type of visualization")
    interactive_features: List[str] = Field(default=[], description="Requested interactive features")

class UserAnalytics(BaseModel):
    """User learning analytics"""
    user_id: str = Field(..., description="User identifier")
    algorithms_studied: List[str] = Field(..., description="Algorithms studied")
    difficulty_progression: Dict[str, int] = Field(..., description="Difficulty level progression")
    time_spent: float = Field(..., description="Total time spent (hours)")
    performance_trends: List[Dict[str, Any]] = Field(..., description="Performance trend data")
    recommended_next_steps: List[str] = Field(..., description="AI-recommended next steps")

class ErrorResponse(BaseModel):
    """Error response model"""
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Error timestamp")