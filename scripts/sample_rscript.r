library("arm")
# path_v <- c(Sys.getenv("RSTATIC"), '/crime_counts.csv')
# a <- read.table(paste(path_v, collapse=""), header=T)
a <- read.table('/Users/mcchang/Dropbox/School/S11/CS194/final_project/static/crime_counts.csv', header=T)
attach(a)

fit.0 <- lm(crime_count ~ distance)
display(fit.0)
plot(fit.0)

crime_count.jitter <- jitter(crime_count)

jitter.distance <- jitter(distance)

