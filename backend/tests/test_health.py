"""
Tests for health check endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint_returns_200(client):
    """Test that health endpoint returns 200 status"""
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_endpoint_structure(client):
    """Test that health endpoint returns correct structure"""
    response = client.get("/api/health")
    data = response.json()
    
    assert "status" in data
    assert "api" in data
    assert "redis" in data
    assert "environment" in data
    assert "llm_provider" in data


def test_health_api_running(client):
    """Test that API is reported as running"""
    response = client.get("/api/health")
    data = response.json()
    
    assert data["api"] == "running"


def test_health_environment_set(client):
    """Test that environment is set"""
    response = client.get("/api/health")
    data = response.json()
    
    assert data["environment"] is not None
    assert isinstance(data["environment"], str)


def test_health_llm_provider_set(client):
    """Test that LLM provider is set"""
    response = client.get("/api/health")
    data = response.json()
    
    assert data["llm_provider"] is not None
    assert isinstance(data["llm_provider"], str)

