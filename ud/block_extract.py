import sys
import pysam

bamfile = sys.argv[1]
chrom = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])
name = sys.argv[5]

samfile = pysam.AlignmentFile(bamfile)

for read in samfile.fetch(chrom,start,end):
    if read.is_secondary:
        continue
    if read.is_supplementary:
        continue
    if read.is_unmapped:
        continue
    if read.reference_start > start:
        continue
    if read.reference_end < end:
        continue
    q_start = None
    q_end = None
    for q,r in read.get_aligned_pairs():
        if q == None:
            continue
        if r == None:
            continue
        if r == start:
            #if r < start:
            q_start = q
        if r == end:
            q_end = q
        # q_end = q        
        # if r > end:
        #     break
    if None in [q_start,q_end]:
        continue
    print(">seq=%s_chrom=%s_start=%s_end=%s_name=%s" % (read.query_name,chrom,start,end,name))
    #print(">%s" % read.query_name)
    print("%s" % read.query_sequence[q_start:q_end])
