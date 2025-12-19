FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Singapore

# 基础工具和媒体工具
RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates bash wget tar xz-utils unzip \
        python3 python3-pip \
        ffmpeg \
        vainfo intel-media-va-driver-non-free i965-va-driver \
        software-properties-common; \
    rm -rf /var/lib/apt/lists/*

# 安装 ImageMagick 编译依赖库
RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # 编译工具
        build-essential pkg-config \
        # 图像格式支持库
        libjpeg-dev libpng-dev libtiff-dev libwebp-dev libheif-dev \
        libfreetype6-dev libfontconfig1-dev \
        # X11 和显示支持
        libx11-dev libxext-dev libxt-dev libxrender-dev libxau-dev libxdmcp-dev \
        # 数学和科学计算
        libfftw3-dev liblqr-1-0-dev \
        # 压缩格式支持
        liblzma-dev libbz2-dev libzstd-dev \
        # 字体和文本处理
        libxft-dev \
        # 颜色管理
        liblcms2-dev \
        # 动画和视频
        libgif-dev libopenjp2-7-dev \
        # 其他图像格式
        libraw-dev libopenexr-dev \
        # 运行时库
        libltdl7 libltdl-dev; \
    rm -rf /var/lib/apt/lists/*

# 编译安装 ImageMagick 7.1.2-11
RUN set -eux; \
    # 下载 ImageMagick 7.1.2-11 源码（使用 GitHub tags）
    cd /tmp && \
    wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.2-11.zip && \
    unzip 7.1.2-11.zip && \
    cd ImageMagick-7.1.2-11 && \
    # 配置编译选项（启用所有特性）
    ./configure \
        --prefix=/usr/local \
        --enable-shared \
        --enable-static \
        --with-modules \
        --with-threads \
        --with-magick-plus-plus \
        --with-quantum-depth=16 \
        --with-fftw \
        --with-lqr \
        --with-lcms \
        --with-lcms2 \
        --with-x \
        --with-xml \
        --with-zlib \
        --with-bzlib \
        --with-lzma \
        --with-zstd \
        --with-jpeg \
        --with-jp2 \
        --with-png \
        --with-tiff \
        --with-webp \
        --with-heif \
        --with-raw \
        --with-openexr \
        --with-gif \
        --with-freetype \
        --with-fontconfig \
        --with-xft \
        --with-rsvg \
        --with-wmf \
        --with-opencl \
        --with-gslib \
        --with-gvc \
        --disable-docs \
        --disable-openmp; \
    # 编译和安装
    make -j$(nproc) && \
    make install && \
    # 更新库路径
    ldconfig && \
    # 清理编译文件和工具
    cd / && \
    rm -rf /tmp/ImageMagick-7.1.2-11* /tmp/7.1.2-11.zip && \
    apt-get remove -y build-essential pkg-config && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    # 验证安装
    /usr/local/bin/magick -version

WORKDIR /app
RUN python3 -m pip install --no-cache-dir --upgrade pip \
 && python3 -m pip install --no-cache-dir mcp spotdl==4.4.3 yt-dlp
COPY server.py /app/server.py

# —— 默认 HTTP/SSE 模式 ——
ENV MCP_MODE=http
ENV MCP_PORT=8080

# —— 创建 SpotDL 配置目录并复制配置文件 ——
RUN mkdir -p /root/.spotdl
COPY config/spotdl/config.json /root/.spotdl/config.json

EXPOSE 8080
CMD ["python3", "server.py"]
