FROM grobid/grobid:0.7.2

EXPOSE 8070

#  enable model preloading
RUN sed -i 's/modelPreload: false/modelPreload: true/g' /opt/grobid/grobid-home/config/grobid.yaml