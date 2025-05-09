library(entropy)
setwd("C:/Users/Julie/Documents/OneDrive/Documents/python for final")
#
data = read.csv('data/test_set.tsv', sep = '\t', strip.white = TRUE)
data.sub = droplevels(data[data$code != 'ERROR',])
data.para = droplevels(data[data$spanish.prep.found == 'para',])
data.por = droplevels(data[data$spanish.prep.found == 'por',])

###################
# generate tables #
###################
prop.table(xtabs(~ data.sub$spanish.prep.found + data.sub$translated.to),1) 
# for split per type
prop.table(xtabs(~ data.para$code))
prop.table(xtabs(~ data.por$code))
# for overall
#fisher.test(xtabs(~ data.sub$spanish.prep.found + data.sub$translated.to),workspace = 2e9)
# significance testing for difference between ontological categories--doesn't translate to prepositions well

#############################
# calculate Shannon-entropy #
#############################
df = data.frame(prop.table(xtabs(~ data.sub$spanish.prep.found + data.sub$code),1))
p.function.para = df[df$data.sub.spanish.prep.found == 'para',]$Freq
p.function.por = df[df$data.sub.spanish.prep.found == 'por',]$Freq
smooth = 0.000001
H.para = -sum((p.function.para+smooth) * log2(p.function.para+smooth))
H.por = -sum((p.function.por+smooth) * log2(p.function.por+smooth))
show(H.para)
show(H.por)