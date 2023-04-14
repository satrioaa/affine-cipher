import cv2 
import math
import numpy as np
import random
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

class Affine:
    def __init__(self, a, b, m ):
        self.a = 9
        self.b = 213
        self.m = 256
        while self.IsCoprime() is False:
            print(a," and ",m," Must be Coprime! ")
            a,m = map(int,input("Enter a and m (Seperated by single space): ").split(" "))
            self.a = a
            self.m = m
        self.inv_a =  self.ModInv()

    def IsCoprime(self):
        """
        Check whether a and m is prime or not. If it is prime then it return true else false
        """
        if math.gcd(self.a, self.m) == 1:
            return True
        return False

    def ModInv(self):
        """
        Form equation 1 = inv(a)*a mod m. we find inv(a)
        Inverse exist only if a and m be Coprime
        """
        for i in range(2,self.m):
            if (self.a * i) % self.m == 1 :
                return i
        return 1
 
    def E(self, x):
        """
        m is the length of range. a and b are the Keys of the cipher.
        The value a must be chosen such that a and are coprime.
        """
        
        return (self.a*x + self.b) % self.m

    def D(self,y):
        """
        Decryption at pixel level
        """
        return (self.inv_a * (y-self.b)) % self.m

    def encryption(self, original_img):
        """
        Encryption of image 
        """
        height = original_img.shape[0]
        width = original_img.shape[1]
        
        for i in range(0,height):
            for j in range(0,width):
                a = original_img[i][j]      # rgb list
                r = self.E(a[0])
                g = self.E(a[1])
                b = self.E(a[2])
                original_img[i][j] = [r,g,b]
        
        cv2.imwrite('encrypted_img.png', original_img)  # saving encrypted image

    def decryption(self, encry_img):
        """
        Decryption of image 
        """
        height = encry_img.shape[0]
        width = encry_img.shape[1]

        for i in range(0,height):
            for j in range(0,width):
                a = encry_img[i][j]         # rgb list
                r = self.D(a[0])
                g = self.D(a[1])
                b = self.D(a[2])
                encry_img[i][j] = [r,g,b]

        cv2.imwrite('decrypted_img.png', encry_img)   # Saving decrypted image
        
    def mse(img1, img2):
        """Calculate Mean Squared Error (MSE) between two images."""
        mse = np.mean((img1 - img2) ** 2)
        return mse
        
class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Affine Cipher")

        self.label = tk.Label(master, text="Affine Cipher")
        self.label.pack()

        self.greet_button = tk.Button(master, text="Encrypt", command=self.encrypt)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Decrypt", command=self.decrypt)
        self.close_button.pack()
        
        self.mse_label = tk.Label(master, text="MSE:")
        self.mse_label.pack()

        
    def show_encrypted_image(self):
        img = Image.open('encrypted_img.png')
        img = img.resize((300, 200))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.master, image=img)
        panel.image = img
        panel.pack()
        
    def show_decrypted_image(self):
        img = Image.open('decrypted_img.png')
        img = img.resize((300, 200))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.master, image=img)
        panel.image = img
        panel.pack()

    def encrypt(self):
        """
        Encrypt the image
        """
        root.filename =  filedialog.askopenfilename(initialdir = "/C:/Users/Satzky/Documents/KULIAH/Smt 6/Kripto",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        img = cv2.imread(root.filename)
        a = random.randint(1,255)
        b = random.randint(1,255)
        m = 256
        affine = Affine(a,b,m)
        affine.encryption(img)
        img2 = cv2.imread('encrypted_img.png')
        mse_result = Affine.mse(img, img2)
        self.mse_label.config(text=f"MSE: {mse_result:.2f}")
        self.show_encrypted_image()
        messagebox.showinfo("Encryption", "Encryption Done")

    def decrypt(self):
        """
        Decrypt the image
        """
        img = cv2.imread('encrypted_img.png')
        a = random.randint(1,255)
        b = random.randint(1,255)
        m = 256
        
        affine = Affine(a,b,m)
        affine.decryption(img)
        img2 = cv2.imread('decrypted_img.png')
        mse_result = Affine.mse(img, img2)
        self.mse_label.config(text=f"MSE: {mse_result:.2f}")
        self.show_decrypted_image()
        messagebox.showinfo("Decryption", "Decryption Done")

    
    def show_image(self, filename):
        img = Image.open(filename)
        img = img.resize((500, 500))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.master, image=img)
        panel.image = img
        panel.pack()
        
    def mse(self):
        """Calculate Mean Squared Error (MSE) between encrypted and decrypted images."""
        encrypted_img = cv2.imread('encrypted_img.png')
        decrypted_img = cv2.imread('decrypted_img.png')
        mse_value = Affine.mse(encrypted_img, decrypted_img)
        messagebox.showinfo("MSE", f"MSE value: {mse_value}")
        
if __name__ == "__main__":
    root = tk.Tk()
    my_gui = GUI(root)
    root.mainloop()