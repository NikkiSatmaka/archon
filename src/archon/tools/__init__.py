from pydantic_ai import RunContext

from archon.pipeline.context import PipelineContext
from archon.service_catalog import search_services
from archon.service_catalog.base import Service


async def web_search(ctx: RunContext[PipelineContext], query: str) -> str:
    """Search the web for cloud provider documentation, pricing, or best practices."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                'https://api.duckduckgo.com/',
                params={'q': query, 'format': 'json', 'no_html': '1'},
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get('AbstractText', '') or str(data.get('Results', []))
            return f'Search returned status {resp.status_code}'
    except ImportError:
        return 'Web search unavailable: httpx not installed'
    except Exception as e:
        return f'Web search failed: {e}'


async def lookup_service(ctx: RunContext[PipelineContext], query: str) -> list[Service]:
    """Search the built-in service catalog for cloud services matching the query."""
    return search_services(query)


async def calculate(ctx: RunContext[PipelineContext], expression: str) -> float:
    """Safely evaluate a mathematical expression for cost estimation.

    Supports: +, -, *, /, **, parentheses, negative numbers.
    """
    import ast

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            val = node.value
            if isinstance(val, (int, float)):
                return float(val)
            raise ValueError(f'Unsupported constant: {val}')
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            raise ValueError(f'Unsupported operator: {type(node.op).__name__}')
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            if isinstance(node.op, ast.UAdd):
                return operand
            raise ValueError(f'Unsupported unary operator: {type(node.op).__name__}')
        raise ValueError(f'Unsupported expression: {type(node).__name__}')

    return _eval(ast.parse(expression, mode='eval'))
