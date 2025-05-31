FROM --platform=linux/amd64 mcr.microsoft.com/dotnet/sdk:2.1

WORKDIR /code

ADD src/Worker /code/src/Worker

RUN dotnet restore -v minimal src/Worker \
    && dotnet publish -c Release -o /code/out src/Worker

CMD ["dotnet", "/code/out/Worker.dll"]
