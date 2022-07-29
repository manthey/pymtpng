import ctypes

MTPNG_THREADS_DEFAULT = 0

MTPNG_RESULT_OK = 0
MTPNG_RESULT_ERR = 1

MTPNG_FILTER_ADAPTIVE = -1
MTPNG_FILTER_NONE = 0
MTPNG_FILTER_SUB = 1
MTPNG_FILTER_UP = 2
MTPNG_FILTER_AVERAGE = 3
MTPNG_FILTER_PAETH = 4

MTPNG_STRATEGY_ADAPTIVE = -1
MTPNG_STRATEGY_DEFAULT = 0
MTPNG_STRATEGY_FILTERED = 1
MTPNG_STRATEGY_HUFFMAN = 2
MTPNG_STRATEGY_RLE = 3
MTPNG_STRATEGY_FIXED = 4

MTPNG_COMPRESSION_LEVEL_FAST = 1
MTPNG_COMPRESSION_LEVEL_DEFAULT = 6
MTPNG_COMPRESSION_LEVEL_HIGH = 9

MTPNG_COLOR_GREYSCALE = 0
MTPNG_COLOR_TRUECOLOR = 2
MTPNG_COLOR_INDEXED_COLOR = 3
MTPNG_COLOR_GREYSCALE_ALPHA = 4
MTPNG_COLOR_TRUECOLOR_ALPHA = 6


try:
    _mtpng = ctypes.cdll.LoadLibrary('libmtpng.so')
except Exception:
    import os

    _libpath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(
        __file__))), 'pymtpng.libs'))
    _lastcount = 0
    while True:
        _count = 0
        for _libname in os.listdir(_libpath):
            try:
                _lib = ctypes.cdll.LoadLibrary(os.path.join(_libpath, _libname))
                _count += 1
                if 'libmtpng' in _libname:
                    _mtpng = _lib
            except Exception:
                pass
        if _count == _lastcount:
            break
        _lastcount = _count
    del _lib
    del _lastcount
    del _count
    del _libpath
    del _libname
    del os


class MtpngError(Exception):
    pass


def mtpng_threadpool_new(threads=MTPNG_THREADS_DEFAULT):
    pp_pool = ctypes.POINTER(ctypes.c_void_p)(ctypes.c_void_p(None))
    if _mtpng.mtpng_threadpool_new(pp_pool, ctypes.c_size_t(threads)):
        raise MtpngError()
    return ctypes.c_void_p(pp_pool[0])


def mtpng_threadpool_release(p_pool):
    pp_pool = ctypes.POINTER(ctypes.c_void_p)(p_pool)
    if _mtpng.mtpng_threadpool_release(pp_pool):
        raise MtpngError()


def mtpng_encoder_options_new():
    pp_options = ctypes.POINTER(ctypes.c_void_p)(ctypes.c_void_p(None))
    if _mtpng.mtpng_encoder_options_new(pp_options):
        raise MtpngError()
    return ctypes.c_void_p(pp_options[0])


def mtpng_encoder_options_release(p_options):
    pp_options = ctypes.POINTER(ctypes.c_void_p)(p_options)
    if _mtpng.mtpng_encoder_options_release(pp_options):
        raise MtpngError()


def mtpng_encoder_options_set_thread_pool(p_options, p_pool):
    if _mtpng.mtpng_encoder_options_set_thread_pool(p_options, p_pool):
        raise MtpngError()


def mtpng_encoder_options_set_filter(p_options, filter_mode):
    if _mtpng.mtpng_encoder_options_set_filter(p_options, ctypes.c_int(filter_mode)):
        raise MtpngError()


def mtpng_encoder_options_set_strategy(p_options, strategy_mode):
    if _mtpng.mtpng_encoder_options_set_strategy(p_options, ctypes.c_int(strategy_mode)):
        raise MtpngError()


def mtpng_encoder_options_set_compression_level(p_options, compression_level):
    if _mtpng.mtpng_encoder_options_set_compression_level(
            p_options, ctypes.c_int(compression_level)):
        raise MtpngError()


def mtpng_encoder_options_set_chunk_size(p_options, chunk_size):
    if _mtpng.mtpng_encoder_options_set_chunk_size(p_options, ctypes.c_size_t(chunk_size)):
        raise MtpngError()


def mtpng_header_new():
    pp_header = ctypes.POINTER(ctypes.c_void_p)(ctypes.c_void_p(None))
    if _mtpng.mtpng_header_new(pp_header):
        raise MtpngError()
    return ctypes.c_void_p(pp_header[0])


def mtpng_header_release(p_header):
    pp_header = ctypes.POINTER(ctypes.c_void_p)(p_header)
    if _mtpng.mtpng_header_release(pp_header):
        raise MtpngError()


def mtpng_header_set_size(p_header, width, height):
    if _mtpng.mtpng_header_set_size(
            p_header, ctypes.c_uint32(width), ctypes.c_uint32(height)):
        raise MtpngError()


def mtpng_header_set_color(p_header, color_type, depth):
    if _mtpng.mtpng_header_set_color(p_header, ctypes.c_int(color_type), ctypes.c_uint8(depth)):
        raise MtpngError()


def mtpng_encoder_new(write_func, flush_func, user_data, p_options):
    pp_encoder = ctypes.POINTER(ctypes.c_void_p)(ctypes.c_void_p(None))

    @ctypes.CFUNCTYPE(
        ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
    def wrap_write(user_data, buf, leng):
        buf = ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte * leng)).contents
        write_func(buf)
        return leng

    @ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
    def wrap_flush(user_data):
        flush_func()
        return 1

    if _mtpng.mtpng_encoder_new(
            pp_encoder,
            wrap_write,
            wrap_flush,
            ctypes.c_char_p(user_data),
            p_options):
        raise MtpngError()
    ret = ctypes.c_void_p(pp_encoder[0])
    # keep references
    ret._wrap_write = wrap_write
    ret._wrap_flush = wrap_flush
    return ret


def mtpng_encoder_release(p_encoder):
    pp_encoder = ctypes.POINTER(ctypes.c_void_p)(p_encoder)
    if _mtpng.mtpng_encoder_release(pp_encoder):
        raise MtpngError()


def mtpng_encoder_write_header(p_encoder, p_header):
    if _mtpng.mtpng_encoder_write_header(p_encoder, p_header):
        raise MtpngError()


def mtpng_encoder_write_palette(p_encoder, p_bytes, len):
    if _mtpng.mtpng_encoder_write_palette(
            p_encoder, ctypes.c_char_p(p_bytes), ctypes.c_size_t(len)):
        raise MtpngError()


def mtpng_encoder_write_transparency(p_encoder, p_bytes, len):
    if _mtpng.mtpng_encoder_write_transparency(
            p_encoder, ctypes.c_char_p(p_bytes), ctypes.c_size_t(len)):
        raise MtpngError()


def mtpng_encoder_write_chunk(p_encoder, p_tag, p_bytes, len):
    if _mtpng.mtpng_encoder_write_chunk(
            p_encoder, ctypes.c_char_p(p_tag), ctypes.c_char_p(p_bytes), ctypes.c_size_t(len)):
        raise MtpngError()


def mtpng_encoder_write_image_rows(p_encoder, p_bytes, len):
    if _mtpng.mtpng_encoder_write_image_rows(
            p_encoder, ctypes.c_char_p(p_bytes), ctypes.c_size_t(len)):
        raise MtpngError()


def mtpng_encoder_finish(p_encoder):
    pp_encoder = ctypes.POINTER(ctypes.c_void_p)(p_encoder)
    if _mtpng.mtpng_encoder_finish(pp_encoder):
        raise MtpngError()


def PILtoPNG(img):
    import io

    buf = io.BytesIO()
    tp = mtpng_threadpool_new()
    eo = mtpng_encoder_options_new()
    mtpng_encoder_options_set_filter(eo, MTPNG_FILTER_ADAPTIVE)
    mtpng_encoder_options_set_compression_level(eo, 1)
    mtpng_encoder_options_set_thread_pool(eo, tp)
    mtpng_encoder_options_set_chunk_size(eo, 200000)
    e = mtpng_encoder_new(buf.write, buf.flush, None, eo)
    h = mtpng_header_new()
    mtpng_header_set_size(h, img.width, img.height)
    bits = 8
    mode = img.mode
    if ';' in mode:
        mode, bits = img.mode.split(';', 1)[1]
        bits = int(bits)
    clr = {
        'L': MTPNG_COLOR_GREYSCALE,
        'RGB': MTPNG_COLOR_TRUECOLOR,
        'LA': MTPNG_COLOR_GREYSCALE_ALPHA,
        'RGBA': MTPNG_COLOR_TRUECOLOR_ALPHA
    }
    if mode not in clr:
        img = img.convert('RGB')
        mode, bits = 'RGB', 8
    data = img.tobytes()
    mtpng_header_set_color(h, clr[mode], bits)
    mtpng_encoder_write_header(e, h)
    mtpng_encoder_write_image_rows(e, data, len(data))
    mtpng_header_release(h)
    mtpng_encoder_finish(e)
    mtpng_encoder_options_release(eo)
    mtpng_threadpool_release(tp)
    return buf.getvalue()
