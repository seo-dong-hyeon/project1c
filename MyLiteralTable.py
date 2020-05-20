class LiteralTable: #literal과 관련된 데이터와 연산을 소유하는 클래스로 section 별로 하나씩 인스턴스를 할당한다
    '''literal_list를 비롯한 모든 필드 생성'''
    def __init__(self):
        self.literal_list = []
        self.location_list = []
        # 임시로 litereal들을 저장하는 공간, 후에 LTORG를 만나거나 프로그램 종료 시 저장 데이터를 literal_list로 옮김
        self.tmp_list = []

    '''매개변수로 온 literal과 location을 list에 추가하는 메소드'''
    def put_literal(self, literal, location):
        self.literal_list.append(literal)
        self.location_list.append(location)

    '''인자로 전달된 literal이 어떤 주소를 지칭하는지 알려주는 메소드'''
    def search(self, literal):
        address = -1

        '''순수한 literal만을 얻기 위해 '\n' 문자 제거'''
        literal = literal.rstrip("\n")

        '''literal_list를 순회하다 찾으려는 literal을 발견하면 해당 순번의 location값을 리턴'''
        for i, value in enumerate(self.literal_list):
            if value.find(literal) != -1:
                address = self.location_list[i]
                break

        return address