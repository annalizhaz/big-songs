import glob
from hdf5 import *
from mrjob.job import MRJob


### decades 0: 2000, decade 1: 2010 - 

## calculate delta, which is if words started appearing more
## in a certain decade than a previous decade

def big_trends(decades, trend_factor):
    '''
    inputs: 
        list of decades (as ints) when a term was used
        trend_factor:  the count difference between a term in one decade and another
                for example, if trend_factor == 3, I look for terms that appeared 3 times more than
                the previous decade
    '''

    trends = []
    s = set(decades)
    for i in s:
        if i != 2 and i != 0: 
        #skip decade 2 since we don't have data from 1910s to compare to 20s
        # treat 0 separately to compare to decade 9
            counts = decades.count(i)
            if (i-1) not in s and counts >= trend_factor:
                trends.append((i-1, i))
        elif i == 0:
            counts = decades.count(i)
            if 9 not in s and counts >= trend_factor:
                trends.append((9, i))

    return trends

class DecadeCounts(MRJob):

    def mapper(self, __, line):

        artist_name, song_year, artist_terms, hot = line.split("|")
        # this only yields words with years, does not yields the terms
        # of songs without years
        if int(song_year) in range(1920, 2020):
            decade = int(song_year[2:4])/10
            for t in artist_terms.split(","):
                yield t.lower(), decade

    def combiner(self, term, decades):

        for d in decades:
            yield term, d

    def reducer(self, term, decades):

        trends = big_trends(list(decades), 5)
        if len(trends) > 0: 
            print term, trends
        # self.term_counts[decade] = {}
        # for t in terms:
        #     self.term_counts[decade][t] = (self.term_counts[decade].get(t, 0) + 1)
        # print self.term_counts

if __name__ == '__main__':

    DecadeCounts.run()




