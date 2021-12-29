class Logger:
    def __init__(self):
        self.notfounds = list()

    def add_song_not_found(self, search_entity):
        self.notfounds.append(search_entity)

    def write_not_founds(self):
        if len(self.notfounds) > 0:
            for entity in self.notfounds:
                title, body = entity
                with open('not_founds.txt', 'a') as outfile:
                    line = "[{}]: {}".format(title, body)
                    outfile.write(line)
                    outfile.write("\n")
