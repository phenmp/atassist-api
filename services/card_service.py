class CardService:
    def __init__(self):
        # do something here if needed
        print('CardService Init')

    def updateWithXML(self, element):
        self.name = element.find('name').text
        self.picture = element.find('picture').text
        self.rarity = int(element.find('rarity').text)

        # Get Type
        self.setCardType()

        # Get Show
        self.setShow()
        # Get Traits
        for traits in element.findall('trait'):
            self.trait.append(traits.text)

        # If no level, assume max level
        if not self.level:
            self.level = (self.rarity + 2) * 3

    def updateFrameName(self):
        frame_name = ""

        # Giggitywatts
        if self.type == constants.GIGGITY:
            if self.rarity == 1:
                frame_name = "WattsCommon.png"
            elif self.rarity == 2:
                frame_name = "WattsRare.png"
            elif self.rarity == 3:
                frame_name = "WattsEpic.png"
        elif self.type == constants.COMBO:
            frame_name += constants.RARITY[self.rarity - 1]
            frame_name += "1combo"

            if len(self.trait) == 0:
                frame_name += "no"
            frame_name += "trait"

            if len(self.skills):
                frame_name += str(len(self.skills)) + ".png"
            else:
                frame_name += ".png"
        else:
            # count skills
            skill_count = len(self.skills)

            max_level = self.rarity + 2
            if self.level > (max_level * 2):
                fused = '3'
            elif self.level > max_level:
                fused = '2'
            else:
                fused = '1'

            frame_name += constants.RARITY[self.rarity - 1]
            frame_name += fused

            if self.type == constants.COMBO:
                frame_name += "combo"
            self.level_up = constants.RARITY[self.rarity - 1] + "up"

            if skill_count and len(self.trait) == 0:
                frame_name += "notrait" + str(skill_count)
            elif skill_count and len(self.trait) > 0:
                frame_name += "trait" + str(skill_count)
            elif not skill_count and len(self.trait) > 0:
                frame_name += "trait"

            frame_name += ".png"

        print('[Updating card frame] Card id: {0}\tFrame name from {1} to {2}'.format(self.id, self.frame, frame_name))
        self.frame = frame_name

    def updateStillName(self):
        picture = self.name.replace("'", "")
        picture = picture.replace("!", "")
        picture = picture.replace(":", "")
        picture = picture.replace("-", "")
        picture = picture.replace(" ", "")
        picture = picture.replace(".", "")
        picture = picture.replace("\"", "")

        if self.id > 1000000:
            picture += "Mythic"

        picture = constants.CARD_SHOW_ABBREVIATION[self.show] + "_" + picture + ".png"
        still = "ATback.png"

        for index in range(len(self.stills)):
            if self.stills[index].lower() == picture.lower():
                still = self.stills[index]
                break
        self.still = still

    def createCardImage(self):
        # If giggity just set image to giggity frame and exit
        if self.type == constants.GIGGITY:
            frame = Image.open(getFullPath(self.config.paths.stillsPath, self.frame))
            self.image = frame.resize((253, 354))
            return

        # Open Card images
        frame = Image.open(getFullPath(self.config.paths.framesPath, self.frame))
        still = Image.open(getFullPath(self.config.paths.stillsPath, self.still))

        # Put Still behind frame
        frame_width, frame_height = frame.size
        still_width, still_height = still.size
        frame = frame.resize((int(frame_width * .65), int(frame_height * .65)), Image.BILINEAR)
        frame_width, frame_height = frame.size

        if still_width > 231 or still_height > 331:
            still = still.resize((231, 331), Image.BILINEAR)
            still_width, still_height = still.size

        f_pix = frame.load()
        s_pix = still.load()

        x_off = 20
        y_off = 20

        for x in range(0, still_width):
            for y in range(0, still_height):
                if f_pix[x + x_off, y + y_off][3] == 0:
                    f_pix[x + x_off, y + y_off] = s_pix[x, y]
                elif f_pix[x + x_off, y + y_off][3] <= 200:
                    if still.mode == 'RGBA':
                        r, g, b, a = s_pix[x, y]
                    else:
                        r, g, b = s_pix[x, y]

                    # z,y,x,w = f_pix[x+x_off,y+y_off]
                    f_pix[x + x_off, y + y_off] = (int(r * .5), int(g * .5), int(b * .5), 255)

        # Put skill icons
        counter = 0
        skill_filename = "resources/deck/skills/skill_"
        for img in self.skills:
            skill_img = Image.open(getFullPath(skill_filename + img[0] + ".png"))

            if not (img[2] is None or img[2] == ''):
                if img[2] == '1' or img[2] == '2' or img[2] == '3' or img[2] == '4' or img[2] == '5':
                    img_special = Image.open("resources/deck/skills/skill_special.png")
                else:
                    img_special = Image.open("resources/deck/skills/skill_special_trait.png")
                self.addImage(skill_img, img_special, (0, 0), 1)

            start = (10, frame_height - int(65 + 45 * counter))
            self.addImage(frame, skill_img, start, .5)
            counter += 1

        # Add trait
        # if(len(self.trait) > 0):
        off = 45
        for i in range(len(self.trait)):
            trait_img = Image.open("resources/deck/traits/icon_small_" + self.trait[i] + ".png")
            start = (frame_width - 45, 60 + off * i)
            self.addImage(frame, trait_img, start, .5)

        level = self.level
        if not level:
            level = (self.rarity + 2) * 3
            self.level = level

        # Level up card
        level = self.level
        m = self.rarity + 2

        if self.type != constants.COMBO:
            while level > m:
                level -= m
            for i in range(1, level + 1):
                level_img = Image.open(
                    getFullPath(self.config.paths.framesPath, "{0}{1}.png".format(self.level_up, str(i))))

                up_width, up_height = level_img.size
                level_img = level_img.resize((int(up_width * .65), int(up_height * .65)))
                start = (0, 0)
                self.addImage(frame, level_img, start, 1)

            # If precombo, then draw little arrows
            if self.type == constants.PC:
                pc = Image.open("resources/deck/card_frames/rsz_pc.png")
                self.addImage(frame, pc, (0, 0), 1)

        # Write All texts
        draw = ImageDraw.Draw(frame)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        # draw.text((x, y),"Sample Text",(r,g,b))

        # Draw name of card
        text = self.name
        sizes = ((14, 75, 35), (20, 75, 30), (26, 75, 25))

        size = 0
        if len(text) <= 10:
            size = 2
        elif len(text) <= 20:
            size = 1

        start = (sizes[size][1], sizes[size][2])

        self.drawText(draw, start, sizes[size][0], text)

        # Draw top left level number
        if self.type != constants.COMBO:
            self.drawText(draw, (27, 10), 48, str(level), left=1, drop=2)

        # Draw skill values
        font = ImageFont.truetype(self.config.font, 30)

        counter = 0
        for skill in self.skills:
            x_off = 50
            if int(skill[1]) < 10:
                x_off += 5
            start = (x_off, frame_height - int(62 + 45 * counter))
            draw.text(start, str(skill[1]), (255, 255, 255), font=font)
            counter += 1

        # Draw health and attack
        x_off = 70
        if int(self.health) < 10 or int(self.health) == 11:
            x_off -= 5

        start = (frame_width - x_off, frame_height - int(45))
        font = ImageFont.truetype(self.config.font, 26)
        draw.text(start, str(self.health), (255, 255, 255), font=font)
        x_off = 68

        if int(self.attack) < 10 or int(self.attack) == 11:
            x_off -= 5
        start = (frame_width - x_off, frame_height - int(45 + 38))
        draw.text(start, str(self.attack), (255, 255, 255), font=font)

        # store compiled image
        frame_width, frame_height = frame.size

        frame = frame.crop((6, 6, frame_width - 5, frame_height - 6))

        frame_width, frame_height = frame.size

        self.image = frame

    def drawText(self, draw, start, fontsize, text, color=(255, 255, 255), shadowcolor="black", drop=1, left=0):
        x, y = start
        font = ImageFont.truetype(self.config.font, fontsize)
        draw.text((x - left, y - left), text, font=font, fill=shadowcolor)
        draw.text((x + drop, y + drop), text, font=font, fill=shadowcolor)
        draw.text((x, y), text, color, font=font)

    def addImage(self, orig, addition, location, scale):
        row = location[0]
        col = location[1]

        add_width, add_height = addition.size
        if scale != 1:
            addition = addition.resize((int(add_width * scale), int(add_height * scale)), Image.BILINEAR)
            add_width, add_height = addition.size

        orig_pix = orig.load()
        add_pix = addition.load()

        for x in range(0, add_width):
            for y in range(0, add_height):
                if add_pix[x, y][3] == 255:
                    orig_pix[x + row, y + col] = add_pix[x, y]
