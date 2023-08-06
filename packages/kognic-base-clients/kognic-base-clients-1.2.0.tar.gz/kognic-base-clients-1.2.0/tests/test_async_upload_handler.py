from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from kognic.base_clients.cloud_storage import UploadSpec
from kognic.base_clients.cloud_storage.upload_handler import UploadHandler

pytest_plugins = ('pytest_asyncio', )


@pytest.mark.asyncio
class TestAsyncUploadHandler:

    async def test_upload_file_200(self, httpx_mock: HTTPXMock, put_spec):
        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec.url, match_content=put_spec.content)
        async_upload_handler = UploadHandler(max_retry_attempts=3, max_retry_wait_time=0.1)
        with open(put_spec.path, 'rb') as f:
            await async_upload_handler.upload_file(f, put_spec.url)
        assert len(httpx_mock.get_requests()) == 1

    async def test_upload_file_500_then_200(self, httpx_mock: HTTPXMock, put_spec):
        httpx_mock.add_response(method="PUT", status_code=500, url=put_spec.url, match_content=put_spec.content)
        httpx_mock.add_response(method="PUT", status_code=500, url=put_spec.url, match_content=put_spec.content)
        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec.url, match_content=put_spec.content)
        async_upload_handler = UploadHandler(max_retry_attempts=3, max_retry_wait_time=0.1)
        with open(put_spec.path, 'rb') as f:
            await async_upload_handler.upload_file(f, put_spec.url)
        assert len(httpx_mock.get_requests()) == 3

    async def test_upload_files_local_200(self, httpx_mock: HTTPXMock, put_spec, put_spec_2):
        upload_specs = {
            'random-data.txt': UploadSpec(
                destination=put_spec.url,
                filename=str(put_spec.path),
                content_type="application/octet-stream",
            ),
            'random-data-2.txt': UploadSpec(
                destination=put_spec_2.url,
                filename=str(put_spec_2.path),
                content_type="application/octet-stream",
            ),
        }

        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec.url, match_content=put_spec.content)
        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec_2.url, match_content=put_spec_2.content)
        async_upload_handler = UploadHandler()

        await async_upload_handler.upload_files(upload_specs=upload_specs)
        assert len(httpx_mock.get_requests()) == 2

    async def test_upload_files_file_data_200(self, httpx_mock: HTTPXMock, put_spec, put_spec_2):
        file_content = put_spec.content
        file_content_2 = put_spec_2.content
        upload_specs = {
            'random-data.txt': UploadSpec(
                destination=put_spec.url,
                filename=str(put_spec.path),
                content_type="application/octet-stream",
                data=file_content,
            ),
            'random-data-2.txt': UploadSpec(
                destination=put_spec_2.url,
                filename=str(put_spec_2.path),
                content_type="application/octet-stream",
                data=file_content_2,
            ),
        }

        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec.url, match_content=file_content)
        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec_2.url, match_content=file_content_2)

        async_upload_handler = UploadHandler()

        await async_upload_handler.upload_files(upload_specs=upload_specs)
        assert len(httpx_mock.get_requests()) == 2

    async def test_upload_files_callback_200(self, httpx_mock: HTTPXMock, put_spec, put_spec_2):
        upload_specs = {
            'random-data.txt': UploadSpec(
                destination=put_spec.url,
                filename=str(put_spec.path),
                content_type="application/octet-stream",
                callback=lambda fname: Path(fname).open('rb'),
            ),
            "random-data-2.txt": UploadSpec(
                destination=put_spec_2.url,
                filename=str(put_spec_2.path),
                content_type="application/octet-stream",
                callback=lambda fname: Path(fname).open('rb').read(),
            ),
        }

        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec.url, match_content=put_spec.content)
        httpx_mock.add_response(method="PUT", status_code=200, url=put_spec_2.url, match_content=put_spec_2.content)

        async_upload_handler = UploadHandler()

        await async_upload_handler.upload_files(upload_specs=upload_specs)
        assert len(httpx_mock.get_requests()) == 2
