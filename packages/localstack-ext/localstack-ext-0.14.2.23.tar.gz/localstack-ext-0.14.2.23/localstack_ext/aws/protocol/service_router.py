from localstack.aws.protocol import service_router as localstack_service_router
from localstack.utils.patch import patch
def patch_service_router():
 import re
 from typing import Callable,Optional
 from localstack.aws.spec import ServiceCatalog
 from localstack.http import Request
 from localstack.services.apigateway.context import ApiInvocationContext
 from localstack_ext.services.apigateway.apigateway_extended import(is_custom_domain_api_invocation)
 @patch(localstack_service_router.determine_aws_service_name)
 def determine_aws_service_name(fn:Callable,request:Request,services:ServiceCatalog=localstack_service_router.get_service_catalog(),**kwargs)->Optional[str]:
  result=fn(request=request,services=services,**kwargs)
  if result in["apigatewaymanagementapi"]:
   return "apigateway"
  return result
 @patch(localstack_service_router.custom_signing_name_rules)
 def custom_signing_name_rules(fn:Callable,signing_name:str,path:str,**kwargs)->Optional[str]:
  if signing_name in["rds","docdb","neptune"]:
   return "rds"
  return fn(signing_name,path,**kwargs)
 @patch(localstack_service_router.custom_host_addressing_rules)
 def custom_host_addressing_rules(fn:Callable,host:str,**kwargs)->Optional[str]:
  if ".cloudfront." in host:
   return "cloudfront"
  if "mediastore-" in host:
   return "mediastore-data"
  if ".elb." in host:
   return "elbv2"
  if ".appsync-api." in host:
   return "appsync"
  return fn(host,**kwargs)
 @patch(localstack_service_router.legacy_rules)
 def legacy_rules(fn:Callable,request:Request,**kwargs)->Optional[str]:
  path=request.path
  method=request.method
  data=request.data
  headers=request.headers
  invocation_context=ApiInvocationContext(method,path,data=data,headers=headers)
  if is_custom_domain_api_invocation(invocation_context):
   return "apigateway"
  if re.match(r"/graphql/[a-zA-Z0-9-]+",path):
   return "appsync"
  auth_header=headers.get("authorization","")
  if auth_header.startswith("Bearer "):
   return "apigateway"
  if path.startswith("/_messages_"):
   return "ses"
  if "/2018-06-01/runtime" in path:
   return "lambda"
  return fn(request=request,**kwargs)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
