from aws_cdk import (
    aws_imagebuilder as imagebuilder,
    core as cdk
)

class ImageBuilderStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        imagebuilderimagerecipe = imagebuilder.CfnImageRecipe(
            self,
            "ImageBuilderImageRecipe",
            name="windows-base",
            version="1.1.0",
            components=[
                {"componentArn": "arn:aws:imagebuilder:us-east-1:aws:component/amazon-cloudwatch-agent-windows/x.x.x"},
                {"componentArn": "arn:aws:imagebuilder:us-east-1:aws:component/aws-cli-version-2-windows/x.x.x"},
                {"componentArn": "arn:aws:imagebuilder:us-east-1:aws:component/powershell-windows/x.x.x"},
                {"componentArn": "arn:aws:imagebuilder:us-east-1:aws:component/python-3-windows/x.x.x"},
                {"componentArn": "arn:aws:imagebuilder:us-east-1:aws:component/update-windows/x.x.x"},
            ],
            parent_image="arn:aws:imagebuilder:us-east-1:aws:image/windows-server-2019-english-full-base-x86/x.x.x",
            tags={
                
            }
        )

        imagebuilderdistributionconfiguration = imagebuilder.CfnDistributionConfiguration(
            self,
            "ImageBuilderDistributionConfiguration",
            name="windows-2019-base",
            distributions=[
                {
                    "region": "us-east-1",
                    "amiDistributionConfiguration": {
                        "Name" : f"windows-2019-base-{{{{ imagebuilder:buildDate }}}}",
                        "AmiTags": {"Name": "windows-2019-base"},
                    }
                }
            ],
        )

        imagebuilderinfrastructureconfiguration = imagebuilder.CfnInfrastructureConfiguration(
            self,
            "ImageBuilderInfrastructureConfiguration",
            name="windows-server-2019",
            instance_profile_name="EC2InstanceProfileForImageBuilder",
            key_pair="key",
            terminate_instance_on_failure=True,
        )

        imagebuilderimage = imagebuilder.CfnImage(
            self,
            "ImageBuilderImage",
            distribution_configuration_arn=imagebuilderdistributionconfiguration.ref,
            infrastructure_configuration_arn=imagebuilderinfrastructureconfiguration.ref,
            image_recipe_arn=imagebuilderimagerecipe.ref,
            image_tests_configuration={
                "image_tests_enabled": True,
                "timeout_minutes": 720
            },
            tags={
                
            }
        )

        imagebuilderimagepipeline = imagebuilder.CfnImagePipeline(
            self,
            "ImageBuilderImagePipeline",
            name="vm-windows-server-2019",
            distribution_configuration_arn=imagebuilderdistributionconfiguration.ref,
            infrastructure_configuration_arn=imagebuilderinfrastructureconfiguration.ref,
            image_recipe_arn=imagebuilderimagerecipe.ref,
            image_tests_configuration={
                "image_tests_enabled": True,
                "timeout_minutes": 720
            },
            status="ENABLED",
            tags={
                
            }
        )