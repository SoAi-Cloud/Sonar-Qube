1. Languages - Sonarqube is supporting many languages, 

```
"Python","Kotlin","Go","Terraform","CloudFormation","Kubernetes",
"Docker","AzureResourceManager","YAML","JSON","JavaScript","TypeScript",
"CSS","Ruby","Scala","C#","Java","HTML","JSP","XML","Flex","PHP","VB.NET"
```

1. Generating a user access token
    
    Please navigate to `/account/security`  and visit “Generate Tokens” section and enter a token and select token type as `User Token` and click on `Generate` to generate a token. Copy it and hit  SonarQube endpoint with the following command
    
    ```
    curl -u sqp_faa9f3b5cf4a24f452285f4b60ea585d6c3d202c: http://localhost:9000/api/system/health
    ```
    
2. sqp_9481b0ede2c18d399a85fa55b8e7c75da3b7685c is CPython project token,
3. curl -u sqp_9481b0ede2c18d399a85fa55b8e7c75da3b7685c : 'http://your-sonarqube-instance/api/qualitygates/project_status?projectKey=YourProjectKey'
4. To retrieve analysis results from a project, use the following command:
    
    ```
    curl -u squ_fe3d0161bc61c9cc2195567015eaaae86f2aca28: "http://127.0.0.1:9000/api/issues/search?projects=CPython"
    ```
    
    Sample results:
