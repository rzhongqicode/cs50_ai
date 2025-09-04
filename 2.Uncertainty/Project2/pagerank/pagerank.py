import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    prob_distribution = {page: 0.0 for page in corpus}
    page_num = len(corpus)
    #当该page没有link指向其他page时
    if len(links) == 0:
        for page in prob_distribution:
            prob_distribution[page] = 1/page_num
        return prob_distribution
    else:
        #根据其他page是否在该page的links中，分为两类分别计算
        for page in prob_distribution:
            if page in links:
                prob_distribution[page] = (damping_factor /
                                           len(links) + (1 - damping_factor) / page_num)
            else:
                prob_distribution[page] = (1 - damping_factor) / page_num
        return prob_distribution

    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {page: 0.0 for page in corpus}
    page_list = list(corpus.keys())
    cur_page = random.choice(page_list)
    result[cur_page] += 1.0
    #在接下来的n-1次取page中，每取到一次，就将result中对应的值+1
    for _ in range(n-1):
        prob_distribution = transition_model(corpus, cur_page, damping_factor)
        probabilities = list(prob_distribution.values())
        next_page = random.choices(page_list, weights=probabilities, k=1)[0]
        cur_page = next_page
        result[cur_page] += 1.0
    #每个page的访问次数除以总采样数，计算pagerank
    for page in result:
        result[page] /= n

    return result
    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_num = len(corpus)
    rank_values = {page: 1/page_num for page in corpus}
    while True:
        #用来记录是否所有的pagerank的精度都已经满足
        accuracy_satisfied = True
        for page in rank_values:
            new_rank_value = (1 - damping_factor) / page_num
            for link_page in corpus:
                #对于一个没有links的page，认为它连接到了所有的pages
                if len(corpus[link_page]) == 0:
                    new_rank_value += damping_factor * rank_values[link_page] / page_num

                elif page in corpus[link_page]:
                    new_rank_value += (damping_factor *
                                       rank_values[link_page] / len(corpus[link_page]))
            error = abs(new_rank_value - rank_values[page])
            if error >= 0.001:
                accuracy_satisfied = False
            #更新rank_value的值
            rank_values[page] = new_rank_value
        #all pages的精度都满足，结束迭代
        if accuracy_satisfied:
            break
    return rank_values
    # raise NotImplementedError


if __name__ == "__main__":
    main()
