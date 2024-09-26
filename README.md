# boulder_crawler
webcrawler for the website sportsnow.ch to get a free spot in the boulder gym
## Fixed Settings
- Crawler Interval: 5min
- Page Loading Delay: 1sec
- Browser: Chromium

Docker Image can be downloaded with **docker push enricocirignaco/boulder_crawler:latest**
# Usage
1. clone repo
2. add .env file to directory with your credentials inside
   EMAIL=<your-username>
   PASSWORD=<your-password>
3. run docker container with shared volume: ```docker run -it -v <path-to-your-repo>:/app enricocirignaco/boulder_crawler:latest```
