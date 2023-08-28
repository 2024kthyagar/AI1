import sys; args = sys.argv[1:]
import random
import urllib.request
from PIL import Image
import math

# K-means clustering of an image
num_means = int(args[0])
image_url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.X6UHt-1GoS0yrOdYwSSWXwAAAA%26pid%3DApi&f=1&ipt=d994ec2bd360622d229dedb6cba7a7f89286db28bf96b4e09919f2595c798627&ipo=images"
image = Image.open(urllib.request.urlopen(image_url))
pixels = image.load()
width, height = image.size
#
# num_distinct_colors = len(set([pixels[i, j] for i in range(width) for j in range(height)]))
# most_common_pixel = max(set([pixels[i, j] for i in range(width) for j in range(height)]), key=lambda x: sum([1 for i in range(width) for j in range(height) if pixels[i, j] == x]))
# most_common_pixel_count = sum([1 for i in range(width) for j in range(height) if pixels[i, j] == most_common_pixel])

# Initialize means, pick random pixels
means = [pixels[random.randint(0, width - 1), random.randint(0, height - 1)] for i in range(num_means)]


# Initialize clusters, list of pixels
clusters = [[] for i in range(num_means)]

# Number of pixels changing clusters
num_changes = 0

print("Starting K-means clustering, number of means:", num_means, "image size:", width, "x", height)

# Assign each pixel to a cluster
for i in range(width):
    for j in range(height):
        pixel = pixels[i, j]
        cluster = min(range(num_means), key=lambda x: sum([(a - b) ** 2 for a, b in zip(pixel, means[x])]))
        if (i, j) not in clusters[cluster]:
            num_changes += 1
            clusters[cluster].append((i, j))

print("Done assigning pixels to clusters")

iteration = 0

while num_changes > 0:
    iteration += 1
    print("Iteration", iteration)
    print("Number of changes:", num_changes)
    # Update means
    for i in range(num_means):
        if len(clusters[i]) > 0:
            means[i] = [sum([pixels[x, y][j] for x, y in clusters[i]]) / len(clusters[i]) for j in range(3)]

    # Reassign pixels to clusters
    num_changes = 0
    for i in range(num_means):
        for pixel in clusters[i]:
            p = pixels[pixel]
            cluster = min(range(num_means), key=lambda x: sum([(a - b) ** 2 for a, b in zip(p, means[x])]))
            if cluster != i:
                clusters[i].remove(pixel)
                clusters[cluster].append(pixel)
                num_changes += 1

# Replace pixels with mean
for i in range(num_means):
    for pixel in clusters[i]:
        pixels[pixel] = tuple([int(x) for x in means[i]])

# Display image
image.show()

# Print stuff
print("Size:", width, "x", height)
print("Pixels:", width * height)
# print("Number of distinct colors:", num_distinct_colors)
print("Number of means:", num_means)
# print("Most common pixel:", most_common_pixel)
# print("Most common pixel count:", most_common_pixel_count)

for i, mean in enumerate(means):
    print("Mean", i, ":", mean, "pixels:", len(clusters[i]))








