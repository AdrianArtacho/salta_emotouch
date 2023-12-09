import pandas as pd
import matplotlib.pyplot as plt

def main(df):
    # Convert 'subject_music' and 'subject_dance' to integers
    df['subject_music'] = df['subject_music'].astype(int)
    df['subject_dance'] = df['subject_dance'].astype(int)

    # Extract the lower age bound and create a new column for sorting
    df['age_lower_bound'] = df['subject_age'].apply(lambda x: int(x.split('-')[0]))

    # Sort the DataFrame based on the new column
    df = df.sort_values(by='age_lower_bound')

    # Calculate total number of subjects and gender percentages
    total_subjects = len(df)
    gender_percentages = df['subject_gender'].value_counts(normalize=True) * 100

    # Create a scatter plot
    plt.figure(figsize=(10, 6))

    # Plotting music and dance competence
    plt.scatter(df['subject_age'], df['subject_music'], color='blue', label='Music Competence')
    plt.plot(df['subject_age'], df['subject_music'], color='blue', alpha=0.5)
    plt.scatter(df['subject_age'], df['subject_dance'], color='green', label='Dance Competence')
    plt.plot(df['subject_age'], df['subject_dance'], color='green', alpha=0.5)

    plt.xlabel('Subject Age')
    plt.ylabel('Competence Score')
    plt.title('Subjective Competence in Music and Dance by Age')

    # Add text annotations for total subjects and gender percentages
    gender_text = '\n'.join([f'{gender}: {percentage:.2f}%' for gender, percentage in gender_percentages.items()])
    stats_text = f'Total Subjects: {total_subjects}\nGender Distribution:\n{gender_text}'
    plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=9, verticalalignment='top')

    plt.legend()
    plt.savefig('METADATA/subject_competence_by_age.png')
    plt.show()

if __name__ == "__main__":
    # Sample DataFrame (replace with your actual DataFrame)
    data = {
        'subject_age': ['35-44', '18-24', '65-75'],
        'subject_music': [3, 2, 5],
        'subject_dance': [5, 3, 1],
        'subject_gender': ['male', 'female', 'non-binary / other']
    }
    df = pd.DataFrame(data)
    main(df)
