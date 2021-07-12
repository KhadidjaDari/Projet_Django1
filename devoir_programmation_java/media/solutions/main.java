
import java.util.*;
 class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner c =new Scanner(System.in);
        int N=c.nextInt();
        int fct=1;
        for(int i=N;i>=1;i--){
        fct=fct*i;
        }

        System.out.print(fct);
        
    }
    
}
