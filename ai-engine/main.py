"""
AlgoMaster-Studio-AI AI Engine
Revolutionary AI-powered algorithm learning platform
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import asyncio
import uvicorn
from datetime import datetime

from services.code_analyzer import CodeAnalyzer
from services.ai_explainer import AIExplainer
from services.performance_benchmarker import PerformanceBenchmarker
from services.visualization_generator import VisualizationGenerator
from models.algorithm_models import AlgorithmRequest, AnalysisResponse
from utils.security import verify_token
from utils.logger import setup_logger

# Initialize FastAPI app
app = FastAPI(
    title="AlgoMaster-Studio-AI AI Engine",
    description="Revolutionary AI-powered algorithm analysis and learning platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
logger = setup_logger("ai-engine")

# Initialize AI services
code_analyzer = CodeAnalyzer()
ai_explainer = AIExplainer()
performance_benchmarker = PerformanceBenchmarker()
visualization_generator = VisualizationGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialize AI engine services on startup"""
    logger.info("🚀 AlgoMaster-Studio-AI AI Engine starting up...")
    await code_analyzer.initialize()
    await ai_explainer.initialize()
    logger.info("✅ AI Engine ready for revolutionary algorithm learning!")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "AlgoMaster-Studio-AI AI Engine",
        "status": "🚀 Revolutionary AI-powered algorithm learning",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "🤖 AI Code Analysis",
            "📊 Performance Benchmarking", 
            "🎨 Interactive Visualizations",
            "💡 Smart Explanations",
            "🔄 Multi-language Support"
        ]
    }

@app.post("/analyze/algorithm", response_model=AnalysisResponse)
async def analyze_algorithm(
    request: AlgorithmRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Revolutionary AI-powered algorithm analysis
    
    Features:
    - Time/Space complexity analysis
    - Code quality assessment
    - Optimization suggestions
    - Visual explanations
    - Performance benchmarking
    """
    try:
        # Verify authentication
        user_id = await verify_token(credentials.credentials)
        
        logger.info(f"🔍 Analyzing algorithm: {request.algorithm_name} for user: {user_id}")
        
        # Comprehensive AI analysis
        analysis_tasks = await asyncio.gather(
            code_analyzer.analyze_complexity(request.code, request.language),
            code_analyzer.assess_quality(request.code, request.language),
            ai_explainer.generate_explanation(request.code, request.language),
            performance_benchmarker.benchmark_algorithm(request.code, request.test_cases),
            visualization_generator.create_flow_diagram(request.code, request.language)
        )
        
        complexity_analysis, quality_assessment, ai_explanation, benchmark_results, visualization = analysis_tasks
        
        # Generate optimization suggestions
        optimization_suggestions = await ai_explainer.suggest_optimizations(
            request.code, complexity_analysis, quality_assessment
        )
        
        response = AnalysisResponse(
            algorithm_name=request.algorithm_name,
            language=request.language,
            complexity_analysis=complexity_analysis,
            quality_assessment=quality_assessment,
            ai_explanation=ai_explanation,
            optimization_suggestions=optimization_suggestions,
            benchmark_results=benchmark_results,
            visualization=visualization,
            analysis_timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Analysis complete for: {request.algorithm_name}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}"
        )

@app.post("/generate/solution")
async def generate_solution(
    problem_description: str,
    target_language: str,
    difficulty_level: str = "medium",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate AI-powered algorithm solutions"""
    try:
        user_id = await verify_token(credentials.credentials)
        
        logger.info(f"🎯 Generating solution in {target_language} for user: {user_id}")
        
        solution = await ai_explainer.generate_solution(
            problem_description, target_language, difficulty_level
        )
        
        return {
            "problem_description": problem_description,
            "language": target_language,
            "difficulty": difficulty_level,
            "solution": solution,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Solution generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Solution generation failed: {str(e)}"
        )

@app.post("/visualize/algorithm")
async def create_visualization(
    code: str,
    language: str,
    visualization_type: str = "flowchart",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create interactive algorithm visualizations"""
    try:
        user_id = await verify_token(credentials.credentials)
        
        logger.info(f"🎨 Creating {visualization_type} visualization for user: {user_id}")
        
        if visualization_type == "flowchart":
            visualization = await visualization_generator.create_flow_diagram(code, language)
        elif visualization_type == "execution":
            visualization = await visualization_generator.create_execution_trace(code, language)
        elif visualization_type == "complexity":
            visualization = await visualization_generator.create_complexity_graph(code, language)
        else:
            raise ValueError(f"Unsupported visualization type: {visualization_type}")
        
        return {
            "visualization_type": visualization_type,
            "language": language,
            "visualization": visualization,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Visualization creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Visualization creation failed: {str(e)}"
        )

@app.get("/algorithms/library")
async def get_algorithm_library():
    """Get comprehensive algorithm library with AI insights"""
    try:
        library = await code_analyzer.get_algorithm_library()
        return {
            "total_algorithms": len(library),
            "categories": library,
            "ai_recommendations": await ai_explainer.get_learning_recommendations(),
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Library fetch failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Library fetch failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )