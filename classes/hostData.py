
class StringList:
    def __init__(self):
        # lưu pid của client 1101,1102 
        self.strings = []
        # Lưu tên phòng
        self.name = []
        #Thông số của nhân vật của client đó (dòng cuối player)
        self.coordinates = []
        #Phòng đang nhiêu đứa
        self.player = []
        
        self.code = []

    def add_string(self, s, information, roomconnect, pler, code):
        if s not in self.strings:
            self.strings.append(s)
            self.coordinates.append(pler)
            self.name.append(information)
            self.player.append(roomconnect)
            self.code.append(code)
            # print(f"String '{s}' with coordinates {pler}.")
        else:
            index = self.strings.index(s)
            self.coordinates[index] = pler
            self.name[index] = information
            self.player[index] = roomconnect
            self.code[index] = code

        # print(self.strings)
        # print(self.coordinates)
        # print(self.name)
        # print(self.player)
        # print(self.code)

    def add_pler(self, s, pler):
        index = self.strings.index(s)
        self.coordinates[index] = pler
        # print(f"String '{s}' coordinates updated to {pler}.")

    def contains_string(self, s):
        return s in self.strings

    def get_coordinate(self, s):
        index = self.strings.index(s)

        for i in range(len(self.code)):
            if self.code[i] == self.code[index] and self.strings[i] != self.strings[index]:
                additional_index = i
                return self.coordinates[additional_index]

        return "NOPLAY"

    def remove_string(self, s):
        if s in self.strings:
            index = self.strings.index(s)
            del self.strings[index]
            del self.coordinates[index]
            del self.name[index] 
            del self.player[index] 
            del self.code[index]
            print(f"String '{s}' and its coordinates removed from the list.")
        else:
            print(f"String '{s}' not found in the list.")

    def __str__(self):
        # Tạo một chuỗi đại diện cho đối tượng Player
        user_info = [
            ';'.join(self.strings),  # 0
            ';'.join(self.player),  # 0
            ';'.join(self.coordinates),  # 0
            ';'.join(self.name),  # 1
            ';'.join(self.code)  # 1
        ]
        print("user:  " + str(user_info))
        return "#".join(user_info)

    def from_string(self, user_info):
        # chuyển string lấy từ server thành giá trị cho player
        # values = user_info.split(",")
        parts = user_info.split('#')

        # Tách từng phần thành các danh sách tương ứng
        self.strings = parts[0].split(';')
        self.player = parts[1].split(';')
        self.coordinates = parts[2].split(';')
        self.name = parts[3].split(';')
        self.code = parts[4].split(';')
        
        print(self.strings)
        print(self.coordinates)
        print(self.name)
        print(self.player)
        print(self.code)
