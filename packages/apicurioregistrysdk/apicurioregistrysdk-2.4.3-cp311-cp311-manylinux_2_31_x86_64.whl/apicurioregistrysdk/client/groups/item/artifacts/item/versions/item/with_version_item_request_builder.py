from __future__ import annotations
from dataclasses import dataclass
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.response_handler import ResponseHandler
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .......models import error
    from .comments import comments_request_builder
    from .comments.item import with_comment_item_request_builder
    from .meta import meta_request_builder
    from .references import references_request_builder
    from .state import state_request_builder

class WithVersionItemRequestBuilder():
    """
    Manage a single version of a single artifact in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithVersionItemRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception("path_parameters cannot be undefined")
        if request_adapter is None:
            raise Exception("request_adapter cannot be undefined")
        # Url template to use to build the URL for the current request builder
        self.url_template: str = "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/versions/{version}{?dereference*}"

        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter
    
    def comments_by_id(self,id: str) -> with_comment_item_request_builder.WithCommentItemRequestBuilder:
        """
        Manage a single comment
        Args:
            id: Unique identifier of the item
        Returns: with_comment_item_request_builder.WithCommentItemRequestBuilder
        """
        if id is None:
            raise Exception("id cannot be undefined")
        from .comments.item import with_comment_item_request_builder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["commentId"] = id
        return with_comment_item_request_builder.WithCommentItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def delete(self,request_configuration: Optional[WithVersionItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .......models import error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": error.Error,
            "405": error.Error,
            "500": error.Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithVersionItemRequestBuilderGetRequestConfiguration] = None) -> bytes:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .......models import error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": error.Error,
            "500": error.Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithVersionItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.DELETE
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[WithVersionItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    @property
    def comments(self) -> comments_request_builder.CommentsRequestBuilder:
        """
        Manage a collection of comments for an artifact version
        """
        from .comments import comments_request_builder

        return comments_request_builder.CommentsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def meta(self) -> meta_request_builder.MetaRequestBuilder:
        """
        Manage the metadata for a single version of an artifact in the registry.
        """
        from .meta import meta_request_builder

        return meta_request_builder.MetaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def references(self) -> references_request_builder.ReferencesRequestBuilder:
        """
        Manage the references for a single version of an artifact in the registry.
        """
        from .references import references_request_builder

        return references_request_builder.ReferencesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def state(self) -> state_request_builder.StateRequestBuilder:
        """
        Manage the state of a specific artifact version.
        """
        from .state import state_request_builder

        return state_request_builder.StateRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class WithVersionItemRequestBuilderDeleteRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

    
    @dataclass
    class WithVersionItemRequestBuilderGetQueryParameters():
        """
        Retrieves a single version of the artifact content.  Both the `artifactId` and theunique `version` number must be provided.  The `Content-Type` of the response depends on the artifact type.  In most cases, this is `application/json`, but for some types it may be different (for example, `PROTOBUF`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        """
        # Allows the user to specify if the content should be dereferenced when being returned
        dereference: Optional[bool] = None

    
    @dataclass
    class WithVersionItemRequestBuilderGetRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

        # Request query parameters
        query_parameters: Optional[WithVersionItemRequestBuilder.WithVersionItemRequestBuilderGetQueryParameters] = None

    

