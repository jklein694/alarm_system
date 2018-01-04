# Use an official Python runtime as a parent image
FROM python:3.6

#RUN apt-get -y update
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    git \
    libatlas-base-dev \
    libav-tools  \
    libgtk2.0-dev \
    libjasper-dev \
    libjpeg-dev \
    libopencv-dev \
    libpng-dev \
    libtiff-dev \
    libvtk6-dev \
    pkg-config \
    python-dev \
    python-numpy \
    python-opencv \
    python-pycurl \
    qt5-default \
    unzip \
    webp \
    wget \
    zlib1g-dev
    #&& apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/Itseez/opencv/archive/3.2.0.zip && \
    unzip 3.2.0.zip && \
    rm 3.2.0.zip && \
    cd opencv-3.2.0 && \
    mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \
    ldconfig

RUN ln -s /usr/local/lib/python3.6/site-packages/cv2.cpython-34m.so /usr/local/lib/python3.6/site-packages/cv2.so

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Set the working directory to /app
WORKDIR /alarm_system

# Copy the current directory contents into the container at /app
ADD . /alarm_system

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME Alarm

# Run app.py when the container launches
CMD ["python3", "real_time_object_detection.py"]