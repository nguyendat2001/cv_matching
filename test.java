import java.util.HashMap;


class Solution {
    public int romanToInt(String s) {
        HashMap<Character, Integer> map = new HashMap<Character, Integer>();
        map.put('I', 1);
        map.put('V', 5);
        map.put('X', 10);
        map.put('L', 50);
        map.put('C', 100);
        map.put('D', 500);
        map.put('M', 1000);
        int res = 0;
        for(int i=0;i<s.length()-1;i++){
            int tmp = calcu(s.charAt(i),s.charAt(i+1));
            if(tmp != -1){
                res += tmp;
                i++;
            }else{
                res += map.get(s.charAt(i));
            }
        }
        return res;
    }

    public int calcu(char a1, char a2){
        if(('I' == a1) && ('V'==a2)) return 4;
        else if(('I' == a1) && ('X' == a2)) return 9;
        else if(('X'==a1) && ('L'==a2)) return 40;
        else if(('X'==a1) && ('C'==a2)) return 90;
        else if(('C'==a1) && ('D'==a2)) return 400;
        else if(('C'==a1) && ('M'==a2)) return 900;
        return -1;
    }
}