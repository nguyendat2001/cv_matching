import pandas as pd
from .user_job_class import *

def read_candidate_file_with_questions(file_path):
    """
    Read an Excel or CSV file containing candidate information, including dynamic Question and Answer fields.

    Args:
        file_path (str): Path to the Excel or CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the candidate data.
    """
    # Check file extension to use appropriate reader
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel files.")

    # Expected base columns
    base_columns = [
        "Name",
        "Date of Birth",
        "University",
        "Address",
        "Email",
        "Phone Number",
        "Year Experience",
        "Technical Skills",
        "Certificates",
        "Degrees",
        "Soft Skills",
        "Experience",
        "English Level"
    ]

    # Identify dynamic Question and Answer columns
    dynamic_columns = [col for col in data.columns if col.startswith("Question") or col.startswith("Answer")]
    all_columns = base_columns + dynamic_columns

    # Check for missing base columns
    missing_columns = [col for col in base_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"The following base columns are missing from the file: {', '.join(missing_columns)}")

    # Ensure only expected columns are included
    data = data[all_columns]

    return data, len(dynamic_columns)  # Return only the DataFrame

def map_to_userinfo(df: pd.DataFrame, num_answers: int = 0) -> List[UserInfo]:
    """
    Map the content of a file to UserInfo instances, including dynamic answer fields.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing the data.
        num_answers (int): Number of dynamic answer fields to expect (default 0).

    Returns:
        List[UserInfo]: List of UserInfo instances.
    """
    # Create dynamic model if num_answers is provided
    if num_answers > 0:
        UserInfoModel = create_dynamic_userinfo(num_answers)
    else:
        UserInfoModel = UserInfo  # Use the base model if no dynamic fields

    user_infos = []
    for _, row in df.iterrows():
        # ... (Existing code to handle date_of_birth and year_experience) ...
        date_of_birth = row.get("Date of Birth")
        if pd.isnull(date_of_birth):
            date_of_birth = None  # Handle missing date_of_birth
        elif isinstance(date_of_birth, pd.Timestamp):
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")  # Format date

        # Convert year_experience to int if possible
        year_experience_raw = row.get("Years of Experience")
        if pd.isnull(year_experience_raw):
            year_experience = []
        else:
            try:
                year_experience = [int(float(year_experience_raw))]
            except ValueError:
                year_experience = [year_experience_raw]

        # Get dynamic answer fields from the DataFrame (if they exist)
        answer_fields = {
            f"answer_{i}": row.get(f"Answer {i}", None)
            for i in range(1, num_answers + 1)
        }

        # Create UserInfo instance, including dynamic fields if present
        user_info = UserInfoModel(
            name=row.get("Name", ""),
            date_of_birth=date_of_birth,
            position=row.get("Position", ""),
            email=row.get("Email", ""),
            phone_number=str(row.get("Phone Number", "")),
            university=row.get("University", "").split(", "),
            technical_skill=row.get("Technical Skills", "").split(", "),
            certificate=row.get("Certificates", "").split(", "),
            degree=row.get("Degrees", "").split(", "),
            soft_skill=row.get("Soft Skills", "").split(", "),
            year_experience=row.get("Year Experience", "").split(", "),
            responsibility=row.get("Experience", ""),
            english_level=[str(row.get("English Level", ""))] if not pd.isnull(row.get("English Level")) else [""],
            **answer_fields  # Add dynamic fields if present
        )
        user_infos.append(user_info)

    return user_infos

