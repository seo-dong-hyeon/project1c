class SymbolTable: #symbol과 관련된 데이터와 연산을 소유하는 클래스로 section 별로 하나씩 인스턴스를 할당한다
    '''symbol_list를 비롯한 모든 필드 생성'''
    def __init__(self):
        self.symbol_list = []
        self.location_list = []
        self.extdef_list = []
        self.extref_list = []

    '''매개변수로 온 symbol과 location을 list에 추가하는 메소드'''
    def put_symbol(self, symbol, location):
        self.symbol_list.append(symbol)
        self.location_list.append(location)

    '''매개변수로 온 인덱스의 extdef 변수를 list에 추가하는 메소드'''
    def put_extdef(self, symbol):
        self.extdef_list.append(symbol)

    '''매개변수로 온 인덱스의 extref 변수를 list에 추가하는 메소드'''
    def put_extref(self, symbol):
        self.extref_list.append(symbol)

    '''인자로 전달된 symbol이 어떤 주소를 지칭하는지 알려주는 메소드'''
    def search(self, symbol):
        address = -1

        '''순수한 symbol만을 얻기 위해 '@','#','\n'와 같은 문자 제거'''
        symbol = symbol.rstrip("\n")
        if symbol.find("#") != -1:
            symbol = symbol.replace("#", "")
        if symbol.find("@") != -1:
            symbol = symbol.replace("@", "")

        '''symbol_list를 순회하다 찾으려는 symbol을 발견하면 해당 순번의 location값을 리턴'''
        for i, value in enumerate(self.symbol_list):
            if value.find(symbol) != -1:
                address = self.location_list[i]
                break

        return address



