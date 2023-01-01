import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas

class NLPAUG():
    '''
    https://towardsdatascience.com/text-augmentation-in-few-lines-of-python-code-cdd10cf3cf84

    Github: https://github.com/makcedward/nlpaug
    '''
    def text_augmentation(self, text, augmented_report_num):
        '''
        @return arr[str]
        '''
        aug = nac.KeyboardAug()
        augmented_text_list = aug.augment(text,augmented_report_num)
        return augmented_text_list

def __test():
    nlpaug = NLPAUG()

    text = '''
        Character Augmenter refers to augmenting data at the character level. 
        '''
    augmented_text = NLPAUG.text_augmentation(text,3)

    original_text = text
    print("original_text:")
    print(original_text)
    print("augmented_text:")
    print(augmented_text)

if __name__ == '__main__':
    __test()
