cfn-create-stack:
	aws cloudformation create-stack --stack-name uhohitsgonnarain-stack --template-body file://codepipeline.yaml --capabilities CAPABILITY_NAMED_IAM

# cfn-create-change-set:
# 	aws cloudformation create-change-set --change-set-name $(name) --stack-name uhohitsgonnarain-stack --template-body file://codepipeline.yaml --capabilities CAPABILITY_NAMED_IAM
