import inventory
import augment
import score
import plot
import time

if __name__ == '__main__':
    now = int(time.time())
    scores = []
    with open('dependencies.txt', 'r') as f:
        for line in f:
            gav = inventory.extract_gav(line)
            if gav is None or "groupId" not in gav or "artifactId" not in gav:
                continue
            healthscore = score.health(now, augment.find_date(gav), augment.find_latest(gav))
            print(healthscore)
            scores.append(healthscore)
    plot.plot(scores, 180)
 