
docker run --rm -v /data/gitlab/rdf:/ws -v /data/software/maven/repository:/root/.m2/repository -v ~/.npm:/root/.npm -v ~/.cache:/root/.cache -v ~/.gradle:/root/.gradle -v ~/.ivy2:/root/.ivy2 -v /tmp:/tmp  --workdir /ws bigtop/slaves:trunk-centos-7 bash -l -c "cd bigtop ; ./gradlew allclean"

