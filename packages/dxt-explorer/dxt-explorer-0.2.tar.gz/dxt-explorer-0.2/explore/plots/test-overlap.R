#!/usr/bin/env Rscript

# DXT Explorer Copyright (c) 2021, The Regents of the University of
# California, through Lawrence Berkeley National Laboratory (subject
# to receipt of any required approvals from the U.S. Dept. of Energy). 
# All rights reserved.
# 
# If you have questions about your rights to use or distribute this software,
# please contact Berkeley Lab's Intellectual Property Office at
# IPO@lbl.gov.
# 
# NOTICE.  This Software was developed under funding from the U.S. Department
# of Energy and the U.S. Government consequently retains certain rights.  As
# such, the U.S. Government has been granted for itself and others acting on
# its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
# Software to reproduce, distribute copies to the public, prepare derivative 
# works, and perform publicly and display publicly, and to permit others to do so.

packages <- c(
	'ggplot2',
	'optparse',
	'plyr',
	'plotly',
	'htmlwidgets',
	'wesanderson'
)

# Install packages not yet installed
installed_packages <- packages %in% rownames(installed.packages())

dir.create(path = Sys.getenv("R_LIBS_USER"), showWarnings = FALSE, recursive = TRUE)

if (any(installed_packages == FALSE)) {
	install.packages(packages[!installed_packages], repos='http://cran.us.r-project.org', lib=Sys.getenv("R_LIBS_USER"))
}

# Packages loading
invisible(lapply(packages, library, character.only = TRUE))

option_list = list(
	make_option(
		c('-f', '--file'),
		type = 'character',
		default = NULL, 
	help = 'DXT CSV file name',
	metavar = 'character'
    )
)
 
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

df <- read.csv(file=opt$file, sep = ',')

df$file_id <- as.factor(df$file_id)
df$duration = df$end - df$start

palette <- wes_palette('Zissou1', 100, type = 'continuous')

maximum = max(df$offset) + (max(df$offset) * 0.01)

plot_posix <- ggplot(
	df,
	aes(
        xmin = start,
        xmax = end,
        y = file_id,
		color = ranks
	)) +
	geom_errorbarh(height=0) +
	expand_limits(x = 0) +
	xlab('File offset (bytes)') +
	ylab('Rank #') +
	theme_bw() +
	theme(
		legend.position = "top",
		plot.title = element_text(size = 10),
		strip.background = element_rect(colour = NA, fill = NA)
	)

p_posix <- ggplotly(
		plot_posix,
		width = 1800,
		height = 500,
		tooltip = "text",
		dynamicTicks = TRUE
	) %>%
	layout(
		margin = list(pad = 0),
		legend = list(orientation = "h", x = 0, y = length(df$ranks) + 6),
		autosize = TRUE,
		xaxis = list(title = 'File offset (bytes)', matches = 'x'),
		yaxis = list(title = 'Rank', matches = 'y', fixedrange = FALSE),
		hoverlabel = list(font = list(color = 'white')),
		title = '<b>DXT Explorer</b> Request Spatiality'
	) %>%
	style(
		showlegend = FALSE
	) %>%
	toWebGL()

p <- subplot(
	p_posix,
	nrows = 1,
	titleY = TRUE,
	titleX = TRUE,
	shareX = TRUE,
	shareY = TRUE
)

saveWidget(p, selfcontained = TRUE, 'new-test.html')
