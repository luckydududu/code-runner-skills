# ImageMagick 使用指南

## 版本信息

- **当前版本**: ImageMagick 7.1.2-11 (源码编译)
- **编译方式**: 从官方源码编译，启用全部特性
- **官方文档**: [ImageMagick Documentation](https://imagemagick.org/script/command-line-processing.php)
- **官方网站**: [ImageMagick.org](https://imagemagick.org/)
- **源码下载**: [ImageMagick Source](https://imagemagick.org/script/download.php#linux)

## 概述

ImageMagick 是一个强大的图像处理工具集，支持超过200种图像格式的读取、写入和转换。它提供了丰富的命令行工具用于图像处理、格式转换、尺寸调整、滤镜应用等操作。

## 编译特性

本系统使用的 ImageMagick 是从源码编译的完整版本，启用了以下特性：

### 核心特性
- ✅ **动态和静态库支持** (`--enable-shared --enable-static`)
- ✅ **模块化架构** (`--with-modules`)
- ✅ **多线程支持** (`--with-threads`)
- ✅ **C++ API** (`--with-magick-plus-plus`)
- ✅ **16位量子深度** (`--with-quantum-depth=16`)

### 图像格式支持
- ✅ **JPEG/JP2** (`--with-jpeg --with-jp2`)
- ✅ **PNG** (`--with-png`)
- ✅ **TIFF** (`--with-tiff`)
- ✅ **WebP** (`--with-webp`)
- ✅ **HEIF** (`--with-heif`)
- ✅ **RAW** (`--with-raw`)
- ✅ **OpenEXR** (`--with-openexr`)
- ✅ **GIF** (`--with-gif`)

### 高级特性
- ✅ **FFTW 快速傅里叶变换** (`--with-fftw`)
- ✅ **Liquid Rescale** (`--with-lqr`)
- ✅ **颜色管理** (`--with-lcms --with-lcms2`)
- ✅ **字体支持** (`--with-freetype --with-fontconfig --with-xft`)
- ✅ **SVG 支持** (`--with-rsvg`)
- ✅ **OpenCL 加速** (`--with-opencl`)
- ✅ **Ghostscript** (`--with-gslib`)
- ✅ **Graphviz** (`--with-gvc`)

## 安装信息

### 安装位置
- **可执行文件**: `/usr/local/bin/magick`
- **配置文件**: `/usr/local/etc/ImageMagick-7/`
- **模块目录**: `/usr/local/lib/ImageMagick-7.1.2/modules-Q16/`

### 验证安装
```bash
# 检查版本和特性
magick -version

# 检查支持的格式
magick -list format

# 检查支持的模块
magick -list module
```

## 基本用法

### 主要命令

- `magick` - 统一的图像处理命令（ImageMagick 7.x 新语法）
- `magick identify` - 获取图像信息
- `magick mogrify` - 批量处理图像
- `magick montage` - 图像拼接
- `magick composite` - 图像合成

## 常用参数详解

### magick 命令

#### 基本语法（ImageMagick 7.x）
```bash
magick [选项] 输入文件 [选项] 输出文件
```

**重要说明**：ImageMagick 7.x 版本要求选项按照严格的顺序执行。在提供操作对象图像之前，必须先给出相应的操作选项。

#### ImageMagick 7.x 语法特点

1. **统一命令**：所有操作都通过 `magick` 命令执行
2. **严格顺序**：选项必须在图像文件之前指定
3. **向后兼容**：仍支持传统的 `convert`、`identify` 等命令（作为 `magick` 的别名）

#### 常用选项

##### 图像信息
- `-verbose` - 显示详细信息
- `-debug` - 显示调试信息
- `-list` - 列出支持的格式、颜色等

##### 尺寸调整
- `-resize WIDTHxHEIGHT` - 调整图像尺寸
- `-resize WIDTHxHEIGHT!` - 强制调整尺寸（忽略宽高比）
- `-resize WIDTHxHEIGHT>` - 仅缩小（不放大）
- `-resize WIDTHxHEIGHT<` - 仅放大（不缩小）
- `-scale WIDTHxHEIGHT` - 快速缩放
- `-thumbnail WIDTHxHEIGHT` - 创建缩略图

##### 格式转换
- `-format FORMAT` - 指定输出格式
- `-quality QUALITY` - 设置压缩质量（1-100）

##### 颜色处理
- `-colorspace COLORSPACE` - 转换颜色空间
- `-colors NUMBER` - 减少颜色数量
- `-monochrome` - 转换为黑白图像
- `-negate` - 反转颜色

##### 滤镜效果
- `-blur RADIUS` - 模糊效果
- `-sharpen RADIUS` - 锐化效果
- `-noise RADIUS` - 添加噪点
- `-emboss RADIUS` - 浮雕效果

## ImageMagick 7.x 迁移指南

### 从旧版本迁移

如果您之前使用 ImageMagick 6.x 或更早版本，以下是主要的语法变化：

#### 命令变化
```bash
# 旧版本 (ImageMagick 6.x)
convert input.jpg -resize 800x600 output.jpg
identify image.jpg

# 新版本 (ImageMagick 7.x)
magick input.jpg -resize 800x600 output.jpg
magick identify image.jpg
# 或者使用统一语法
magick image.jpg info:
```

#### 选项顺序
```bash
# 正确：选项在图像文件之前
magick -resize 800x600 input.jpg output.jpg

# 错误：选项在图像文件之后
magick input.jpg -resize 800x600 output.jpg
```

## 使用示例

### 1. 基本格式转换
```bash
# 转换 PNG 到 JPEG
magick input.png output.jpg

# 转换并设置质量
magick input.png -quality 85 output.jpg

# 批量转换
magick *.png -quality 90 output_%d.jpg
```

### 2. 尺寸调整
```bash
# 调整到指定尺寸
magick input.jpg -resize 800x600 output.jpg

# 保持宽高比，最大尺寸
magick input.jpg -resize 800x600> output.jpg

# 创建缩略图
magick input.jpg -thumbnail 200x200 thumbnail.jpg
```

### 3. 图像信息查看
```bash
# 查看图像基本信息
magick identify image.jpg

# 查看详细信息
magick identify -verbose image.jpg

# 查看支持的格式
magick identify -list format

# 或者使用新的统一语法
magick image.jpg -verbose info:
```

### 4. 批量处理
```bash
# 批量调整尺寸
magick mogrify -resize 800x600 *.jpg

# 批量转换格式
magick mogrify -format png *.jpg

# 批量添加水印
magick mogrify -composite -gravity southeast watermark.png *.jpg
```

### 5. 高级处理
```bash
# 图像拼接
magick montage image1.jpg image2.jpg -geometry +10+10 output.jpg

# 图像合成
magick composite -gravity center overlay.png background.jpg output.jpg

# 创建 GIF 动画
magick -delay 20 frame*.png animation.gif
```

## 最佳实践

### 1. 图像优化
```bash
# 压缩 JPEG 图像
magick input.jpg -quality 85 -strip output.jpg

# 优化 PNG 图像
magick input.png -strip -define png:compression-level=9 output.png

# 转换为 WebP 格式
magick input.jpg -quality 90 output.webp
```

### 2. 批量处理
```bash
# 批量创建缩略图
for file in *.jpg; do
    magick "$file" -thumbnail 300x300 "thumb_$file"
done

# 批量调整尺寸并保持质量
magick mogrify -resize 1920x1080> -quality 90 *.jpg
```

### 3. 图像信息提取
```bash
# 获取图像尺寸
magick identify -format "%wx%h" image.jpg

# 获取文件大小
magick identify -format "%b" image.jpg

# 获取颜色信息
magick identify -format "%k colors" image.jpg
```

## 高级用法

### 1. 图像滤镜
```bash
# 应用模糊效果
magick input.jpg -blur 0x3 output.jpg

# 应用锐化效果
magick input.jpg -sharpen 0x1 output.jpg

# 应用浮雕效果
magick input.jpg -emboss 0x1 output.jpg
```

### 2. 颜色处理
```bash
# 转换为灰度
magick input.jpg -colorspace Gray output.jpg

# 调整亮度和对比度
magick input.jpg -brightness-contrast 10x20 output.jpg

# 反转颜色
magick input.jpg -negate output.jpg
```

### 3. 图像合成
```bash
# 添加文字水印
magick input.jpg -pointsize 24 -fill white -annotate +10+10 "Watermark" output.jpg

# 添加图片水印
magick input.jpg watermark.png -gravity southeast -composite output.jpg
```

## 故障排除

### 常见问题

1. **内存不足**
   - 使用 `-limit memory 256MB` 限制内存使用
   - 使用 `-limit map 512MB` 限制映射内存

2. **处理速度慢**
   - 使用 `-threads 4` 启用多线程
   - 使用 `-define registry:temporary-path=/tmp` 指定临时目录

3. **格式不支持**
   - 使用 `identify -list format` 查看支持的格式
   - 安装相应的编解码器

### 调试命令
```bash
# 显示处理过程
magick -verbose input.jpg output.jpg

# 显示内存使用
magick -debug all input.jpg output.jpg

# 测试命令语法
magick -list configure
```

## 注意事项

1. **版权合规**: 请确保您有权处理相关图像内容
2. **文件格式**: 确保输入文件格式被支持
3. **内存使用**: 大图像处理时注意内存限制
4. **备份文件**: 处理重要文件前请先备份
5. **质量设置**: 根据需求调整压缩质量

## 相关链接

- [ImageMagick 官方文档](https://imagemagick.org/script/command-line-processing.php)
- [ImageMagick 7.x 迁移指南](https://imagemagick.org/script/porting.php)
- [ImageMagick 示例](https://imagemagick.org/script/examples.php)
- [ImageMagick 下载页面](https://imagemagick.org/script/download.php)
