import re
import random

BASE_URL = 'http://www.startups-list.com/'
NICE_HREF_EVIDENCES = ['btn', 'label label-default']

def get_page_content(url):
    import urllib.request
    content = ''
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
    return content

def get_href(html_chunk):
    match = re.search(r'href=[\'"]?([^\'" >]+)', html_chunk)
    if match:
        return match.group(0)[6:]
    else:
        return None

def is_nice_href(html_chunk):
    return html_chunk.find('class="btn"') != -1

def get_startup_names(url):
    content = get_page_content(url)
    startup_names = re.findall(r'data-name="(.*?)"', content)
    for i in range(len(startup_names)):
        startup_names[i] = str(startup_names[i].strip())
    return startup_names

def get_geo_located_sites(base_url):
    content = get_page_content(base_url)
    href_chunks = re.findall(r'<a(.*?)\/a>', content)
    nice_hrefs = []
    for item in href_chunks:
        if is_nice_href(item):
            href = get_href(item)
            nice_hrefs.append(href)
    return nice_hrefs

if __name__ == '__main__':
    import time
    print('Listing geolocated sites...')
    pages = get_geo_located_sites(BASE_URL)
    print('Done. We have', len(pages), 'pages to process.')

    results = []
    for page in pages:
        print('  Processing:', page)
        current_results = get_startup_names(page)
        print('  +', len(current_results))
        results.extend(current_results)

        sleep_time = random.randrange(10, 20)
        print('  Sleep:', sleep_time, 'sec')
        time.sleep(sleep_time)

    print('All jobs done!')
    print('Total results number:', len(results))

    print('Saving results...')
    with open('names.txt', 'w') as f:
        for line in results:
            try:
                f.write(line + '\n')
            except:
                print('Something goes wrong with this:', line)

    print('Done!!!')