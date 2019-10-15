import asyncio
import urllib.request
import os
def download(url,file):
    #f = open(file,'wb')
    urllib.request.urlretrieve(url,file)
    #f.close()


def url_gen(url,start=1):
    url_root = url[:url.find('segment')]
    i = start
    while True:
        yield url_root+f'segment{i}.ts'
        i+=1

def segments_gen(url,path,start=1):
    url_root = url[:url.find('segment')]
    i = start
    while True:
        yield (url_root+f'segment{i}.ts',os.path.join(path,f'{i}.ts'))
        i+=1

def download_segments(url,path,start=1):
    url_generator = url_gen(url,start)
    i=start
    try:

        for each in url_generator:
            download(each, os.path.join(path,f'{i}.ts'))
            i+=1
    except urllib.request.HTTPError as e:
        return [n for n in range(start, i)]




def download_segments_parallel(url,path,workers=4,start=1):
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=workers)
    for current_url,name in segments_gen(url,path,start):
        #print(current_url,name)
        try:
            result = executor.submit(download,current_url,name)
            result.result()
        except urllib.request.HTTPError as e:
            return


async def download_segments_parallel2(url,path,start=1):
    import aiohttp
    import aiofiles
    async with aiohttp.ClientSession() as session:
        for current_url, name in segments_gen(url,path,start):
            async with session.get(current_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(name, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                elif resp.status == 404:
                    return




def download_segments_parallel_main(url,path,start):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(download_segments_parallel2(url,path,start))

