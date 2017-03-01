docker rm tiler
docker run --name "tiler" -v /Users/jmilner/Documents/Code/tiler/tiler/tiler-data:/tiler-data -p 25432:5432 tiler