def ram_manager(addr: Variable, rs2: Variable, RAM_read:Variable, RAM_write:Variable, RAM_sign_extend:Variable, RAM_word_size:Variable) -> Variable:
    '''RAM manager implementation'''
    
    return (tmp ^ c, (tmp & c) | (a & b))