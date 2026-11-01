from fastapi import APIRouter

router = APIRouter(prefix='/health', tags=['Default'])


@router.get('/check', summary='Проверка доступности сервиса')
async def health_check() -> dict[str, str]:
    return {'status': 'ok'}
